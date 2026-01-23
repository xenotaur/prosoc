#!/usr/bin/env python
"""
Build Corpus A (valid) and Corpus B (invalid) for auditor experiments.

Corpus A:
  - Original Markdown normative cards with aligned embedded YAML.

Corpus B:
  - Markdown normative cards whose embedded YAML blocks have been
    programmatically replaced with YAML from *different* scenarios,
    preserving all surrounding prose.

This script operates on Markdown-with-embedded-YAML, which is the
*auditable artifact* in the Prosoc Normative Card Architecture.
"""

from pathlib import Path
import random
import sys
import yaml

from prosoc.literate import compiler
from prosoc.utils.experiments import mutator
from prosoc.utils.paths import find_repo_root


RNG_SEED = 42


def main():
    project_root = find_repo_root()

    scenarios_root = project_root / "prosoc" / "scenarios"
    output_root = project_root / "experiments" / "2026_01" / "corpora"

    valid_root = output_root / "valid"
    invalid_root = output_root / "invalid"

    valid_root.mkdir(parents=True, exist_ok=True)
    invalid_root.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------
    # Discover scenario Markdown files
    # ------------------------------------------------------------

    scenarios = []
    for path in scenarios_root.iterdir():
        if not path.is_dir():
            continue
        if path.name in {"schema.json", "template.md", "workflow.md"}:
            continue

        md_path = path / "scenario.md"
        if not md_path.exists():
            continue

        markdown_text = md_path.read_text(encoding="utf-8")
        yaml_blocks = compiler.extract_yaml_blocks(markdown_text)

        yaml_dict = yaml.safe_load(yaml_blocks[0])
        if not isinstance(yaml_dict, dict):
            print(f"Skipping {path.name}: YAML block did not parse to a mapping", file=sys.stderr)
            continue

        scenarios.append({
            "name": path.name,
            "markdown": markdown_text,
            "yaml": yaml_dict,
        })

    if len(scenarios) < 2:
        print("Need at least two scenarios to build scrambled corpus.", file=sys.stderr)
        sys.exit(1)

    print(f"Discovered {len(scenarios)} scenarios.")

    # ------------------------------------------------------------
    # Corpus A: Valid (unaltered normative cards)
    # ------------------------------------------------------------

    for s in scenarios:
        out_dir = valid_root / s["name"]
        out_dir.mkdir(exist_ok=True)

        out_md = out_dir / "scenario.md"
        out_md.write_text(s["markdown"], encoding="utf-8")

    print(f"Wrote Corpus A (valid) to {valid_root}")

    # ------------------------------------------------------------
    # Corpus B: Invalid (scrambled embedded YAML)
    # ------------------------------------------------------------

    rng = random.Random(RNG_SEED)
    yaml_pool = [s["yaml"] for s in scenarios]
    shuffled_yaml = yaml_pool[:]
    rng.shuffle(shuffled_yaml)

    # Ensure no scenario keeps its own YAML
    for i, s in enumerate(scenarios):
        if shuffled_yaml[i] == s["yaml"]:
            swap_idx = (i + 1) % len(shuffled_yaml)
            shuffled_yaml[i], shuffled_yaml[swap_idx] = (
                shuffled_yaml[swap_idx],
                shuffled_yaml[i],
            )

    for s, wrong_yaml in zip(scenarios, shuffled_yaml):
        out_dir = invalid_root / s["name"]
        out_dir.mkdir(exist_ok=True)

        mutated_markdown = mutator.replace_yaml_block(
            markdown_text=s["markdown"],
            new_yaml_dict=wrong_yaml,
        )

        out_md = out_dir / "scenario.md"
        out_md.write_text(mutated_markdown, encoding="utf-8")

    print(f"Wrote Corpus B (invalid) to {invalid_root}")


if __name__ == "__main__":
    main()
