#!/usr/bin/env python
"""
Batch auditor runner for Prosoc normative cards.

This script audits all Markdown normative cards under:
  experiments/2026_01/corpora/valid/**/scenario.md
  experiments/2026_01/corpora/invalid/**/scenario.md

For each card, it:
- runs the Prosoc auditor
- writes one JSON audit report per card
- records failures without stopping the run

It also supports dry-run limits and validates directory structure.
"""

from __future__ import annotations

import json
import traceback
from pathlib import Path
from typing import Dict, List, Iterable

from prosoc.auditor import orchestrator
from prosoc.auditor import openai_client
from prosoc.utils import secrets
from prosoc.utils import paths


EXPERIMENT_ID = "2026_01"

# Dry-run / safety limits (set to None for no limit)
MAX_DIRS_PER_CORPUS = None   # e.g. 2
MAX_FILES_TOTAL = None      # e.g. 3


# -----------------------------
# Helpers
# -----------------------------

def _find_scenario_files(root: Path, *, max_dirs: int | None) -> List[Path]:
    """
    Find scenario.md files exactly one level below root.
    Expected layout:
      root/<scenario_name>/scenario.md
    """
    if not root.exists():
        raise FileNotFoundError(f"Corpus directory does not exist: {root}")

    scenario_dirs = sorted(p for p in root.iterdir() if p.is_dir())

    if max_dirs is not None:
        scenario_dirs = scenario_dirs[:max_dirs]

    files: List[Path] = []
    for d in scenario_dirs:
        md = d / "scenario.md"
        if md.exists():
            files.append(md)

    if not files:
        raise RuntimeError(f"No scenario.md files found under {root}")

    return files



def _audit_files(
    *,
    label: str,
    files: Iterable[Path],
    output_dir: Path,
    llm_client: openai_client.OpenAIClient,
    model_name: str,
    max_files: int | None,
    schema: Dict[str, Any],
    root_key: str,
) -> Dict[str, object]:
    """Audit a collection of scenario Markdown files."""

    print(f"Auditing {label} corpus...")
    results: List[Dict[str, object]] = []
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for md_path in files:
        if max_files is not None and count >= max_files:
            break

        print(f" - Auditing {md_path} ({count + 1}/{len(files)})...")

        count += 1
        card_name = md_path.parent.name
        output_path = output_dir / f"{card_name}.audit.json"

        try:
            markdown_text = md_path.read_text(encoding="utf-8")

            report = orchestrator.audit_markdown_card(
                markdown_text=markdown_text,
                source_path=str(md_path),
                schema=schema,
                root_key=root_key,  # ← scenarios are unrooted
                llm_client=llm_client,
                model_name=model_name,
            )

            output_path.write_text(
                json.dumps(report, indent=2), encoding="utf-8"
            )

            results.append(
                {
                    "card": card_name,
                    "status": report.get("internal_consistency", {}).get("status"),
                    "error_count": report.get("summary", {}).get("error_count", 0),
                    "failed": False,
                }
            )

        except Exception as exc:  # intentional: batch robustness
            output_path.write_text(
                json.dumps(
                    {
                        "card": card_name,
                        "failed": True,
                        "exception": str(exc),
                        "traceback": traceback.format_exc(),
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            results.append(
                {
                    "card": card_name,
                    "status": "failed",
                    "error_count": None,
                    "failed": True,
                }
            )

            print(f"Failed to audit {card_name}: {exc}")

    successful = [r for r in results if not r["failed"]]
    passed = [r for r in successful if r["status"] == "pass"]

    avg_error_count = (
        sum(r["error_count"] for r in successful) / len(successful)
        if successful
        else 0.0
    )

    return {
        "count": len(results),
        "pass_rate": len(passed) / len(results) if results else 0.0,
        "avg_error_count": round(avg_error_count, 3),
        "failures": len([r for r in results if r["failed"]]),
    }


# -----------------------------
# Main entry point
# -----------------------------

def main() -> None:
    repo_root = paths.find_repo_root()

    exp_root = repo_root / "experiments" / EXPERIMENT_ID
    corpora_root = exp_root / "corpora"

    valid_root = corpora_root / "valid"
    invalid_root = corpora_root / "invalid"

    results_root = exp_root / "results"
    valid_out = results_root / "valid"
    invalid_out = results_root / "invalid"

    print("Auditing corpora...")
    print(f" - 'Valid' corpus:   {valid_root}")
    print(f" - 'Invalid' corpus: {invalid_root}")

    valid_files = _find_scenario_files(valid_root, max_dirs=MAX_DIRS_PER_CORPUS)
    invalid_files = _find_scenario_files(invalid_root, max_dirs=MAX_DIRS_PER_CORPUS)

    # Load scenario schema (used for Markdown → YAML extraction)
    schema_path = (
        repo_root / "prosoc" / "scenarios" / "schema.json"
    )

    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)
    root_key = None  # ← scenarios are unrooted

    api_key = secrets.load_openai_api_key()
    llm_client = openai_client.OpenAIClient(api_key=api_key)

    summary = {
        "valid": _audit_files(
            label="valid",
            files=valid_files,
            output_dir=valid_out,
            llm_client=llm_client,
            model_name="default",
            max_files=MAX_FILES_TOTAL,
            schema=schema,
            root_key=root_key,
        ),
        "invalid": _audit_files(
            label="invalid",
            files=invalid_files,
            output_dir=invalid_out,
            llm_client=llm_client,
            model_name="default",
            max_files=MAX_FILES_TOTAL,
            schema=schema,
            root_key=root_key,
        ),
    }

    results_root.mkdir(parents=True, exist_ok=True)
    (results_root / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print("Batch audit complete.")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
