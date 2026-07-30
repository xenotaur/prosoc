#!/usr/bin/env python
"""
Assemble every 2026_07 combinatorics manifest and build a comparison summary.

For each entry in combinations.COMBINATIONS, loads the corresponding
corpora/<id>.yml manifest, assembles a dev-mode packet (--allow-unapproved
equivalent, since the corpus is not yet APPROVED), and writes:

  results/packets/<id>.packet.yml   -- the full assembled envelope
  results/summary.json              -- per-combo principle emphasis + tensions
  results/summary.md                -- human-readable table + highlighted diffs

Run scripts/build_manifests.py first to generate the manifests this script
reads.
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO_ROOT))
from combinations import COMBINATIONS, JUSTIFICATION  # noqa: E402

from prosoc.packet.assemble import assemble  # noqa: E402
from prosoc.packet.errors import PacketError  # noqa: E402
from prosoc.packet.gate import gate  # noqa: E402
from prosoc.packet.manifest import load_manifest  # noqa: E402
from prosoc.packet.resolve import resolve  # noqa: E402

EXPERIMENT_ID = "2026_07"


def _assemble_one(manifest_path: Path) -> dict:
    manifest = load_manifest(manifest_path)
    cards = resolve(manifest)
    result = gate(cards, allow_unapproved=True)
    if not result.passed:
        raise PacketError(
            f"unexpected gate failure even with allow_unapproved=True: "
            f"{[b.reason for b in result.blocked]}"
        )
    return assemble(cards, manifest, allow_unapproved=True, justification=JUSTIFICATION)


def _principle_emphasis(envelope: dict) -> dict[str, str]:
    return {p["id"]: p["emphasis"] for p in envelope["guidance"]["principles"]}


def _tensions(envelope: dict) -> list[str]:
    tensions = envelope["guidance"].get("tensions", {})
    out: list[str] = []
    for entry in tensions.get("common_tensions", []):
        out.extend(entry.get("tensions", []))
    return out


def _write_summary_md(path: Path, rows: list[dict]) -> None:
    lines = [
        "# 2026_07 packet combinatorics — summary",
        "",
        "One assembled packet per (task, context, scenario) combination. See "
        "`combinations.py` for the rationale behind each pick.",
        "",
        "| id | task | context | scenario | emphasized | deprioritized |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        emphasized = ", ".join(
            pid for pid, e in row["principles"].items() if e == "emphasized"
        )
        deprioritized = ", ".join(
            pid for pid, e in row["principles"].items() if e == "deprioritized"
        )
        lines.append(
            f"| `{row['id']}` | {row['task']} | {row['context']} | "
            f"{row['scenario']} | {emphasized} | {deprioritized} |"
        )

    # Highlight same scenario+task, different context pairs -- the clearest
    # proof that context alone changes the assembled guidance.
    lines += ["", "## Highlighted diffs: same scenario + task, different context", ""]
    by_task_scenario: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        by_task_scenario.setdefault((row["task"], row["scenario"]), []).append(row)

    found_pair = False
    for (task, scenario), group in by_task_scenario.items():
        if len(group) < 2:
            continue
        found_pair = True
        lines.append(f"### `{task}` × `{scenario}`, varying context")
        for row in group:
            emphasized = sorted(
                pid for pid, e in row["principles"].items() if e == "emphasized"
            )
            deprioritized = sorted(
                pid for pid, e in row["principles"].items() if e == "deprioritized"
            )
            lines.append(
                f"- **{row['context']}**: emphasized={emphasized}, "
                f"deprioritized={deprioritized}"
            )
        lines.append("")

    if not found_pair:
        lines.append("(no same scenario+task pairs with differing context found)")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    import json

    repo_root = REPO_ROOT
    exp_root = repo_root / "experiments" / EXPERIMENT_ID
    corpora_root = exp_root / "corpora"
    results_root = exp_root / "results"
    packets_root = results_root / "packets"
    packets_root.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    failures: list[dict] = []

    for combo in COMBINATIONS:
        manifest_path = corpora_root / f"{combo.id}.yml"
        print(f"assembling {combo.id} ({manifest_path.name})...")
        try:
            envelope = _assemble_one(manifest_path)
        except Exception as exc:  # intentional: batch robustness
            print(f"  FAILED: {exc}")
            failures.append(
                {
                    "id": combo.id,
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                }
            )
            continue

        packet_path = packets_root / f"{combo.id}.packet.yml"
        packet_path.write_text(
            yaml.safe_dump(envelope, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

        rows.append(
            {
                "id": combo.id,
                "task": combo.task,
                "context": combo.context,
                "scenario": combo.scenario,
                "principles": _principle_emphasis(envelope),
                "tensions": _tensions(envelope),
                "subject_digest": envelope["subject"][0]["digest"]["sha256"],
            }
        )

    results_root.mkdir(parents=True, exist_ok=True)
    (results_root / "summary.json").write_text(
        json.dumps({"combinations": rows, "failures": failures}, indent=2),
        encoding="utf-8",
    )
    _write_summary_md(results_root / "summary.md", rows)

    print(f"\nAssembled {len(rows)}/{len(COMBINATIONS)} packets.")
    if failures:
        print(f"{len(failures)} FAILED — see results/summary.json")
    print(f"Summary written to {results_root / 'summary.md'}")

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
