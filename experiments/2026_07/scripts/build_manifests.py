#!/usr/bin/env python
"""
Build ad-hoc packet manifests for the 2026_07 combinatorics experiment.

For each entry in combinations.COMBINATIONS, writes a manifest YAML naming
the charter, asimov_three_laws, and the entry's (task, context, scenario)
triple. These are ad-hoc manifests for this experiment only -- they are not
registered as prosoc/manifests/ cards, so they carry no STATUS block and are
not subject to prosoc-card-audit. prosoc.packet.manifest.load_manifest reads
any manifest-shaped YAML regardless of where it lives (see
prosoc/packet/README.md, "Scope").
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO_ROOT))
from combinations import COMBINATIONS, CONSTITUTION  # noqa: E402

EXPERIMENT_ID = "2026_07"


def main() -> None:
    repo_root = REPO_ROOT
    corpora_root = repo_root / "experiments" / EXPERIMENT_ID / "corpora"
    corpora_root.mkdir(parents=True, exist_ok=True)

    for combo in COMBINATIONS:
        manifest = {
            "id": combo.id,
            "name": f"{combo.task} / {combo.context} / {combo.scenario}",
            "state": "DRAFTED",
            "builder": "prosoc packet assembler (2026_07 combinatorics experiment)",
            "members": [
                {"family": "charter", "id": "charter"},
                {"family": "constitutions", "id": CONSTITUTION},
                {"family": "scenarios", "id": combo.scenario},
                {"family": "tasks", "id": combo.task},
                {"family": "contexts", "id": combo.context},
            ],
        }

        out_path = corpora_root / f"{combo.id}.yml"
        out_path.write_text(
            yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        print(f"wrote {out_path.relative_to(repo_root)}")

    print(f"\nWrote {len(COMBINATIONS)} manifests to {corpora_root}")


if __name__ == "__main__":
    main()
