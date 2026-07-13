"""
Scenario distillation tool.

This module distills human-authored social navigation scenarios written in
Markdown with fenced YAML blocks into machine-readable YAML files, validated
against the scenario JSON schema.

It supports two layouts:

1. Directory layout (default):
   prosoc/scenarios/<scenario_id>/scenario.md -> scenario.yml

2. Flat layout (legacy / optional):
   prosoc/scenarios/<scenario_id>.md -> <scenario_id>.yml

The core Markdown→YAML logic is delegated to prosoc.literate.compiler.
"""

from __future__ import annotations

import argparse
import pathlib
from typing import Iterable, NamedTuple

from prosoc.literate import compiler
from prosoc.literate import utils

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

SCHEMA_PATH = pathlib.Path(__file__).parent / "schema.json"
DEFAULT_ROOT_KEY = None  # was "scenario"


# -----------------------------------------------------------------------------
# Scenario source abstraction
# -----------------------------------------------------------------------------


class ScenarioSource(NamedTuple):
    md_path: pathlib.Path
    yml_path: pathlib.Path


# -----------------------------------------------------------------------------
# Discovery
# -----------------------------------------------------------------------------


def discover_directory_layout(
    root: pathlib.Path,
    scenario: str | None = None,
) -> Iterable[ScenarioSource]:
    """Discover scenarios using the directory-based layout.

    If `scenario` is given, restrict discovery to the directory whose name
    matches it exactly.
    """
    for child in root.iterdir():
        if not child.is_dir():
            continue
        if scenario is not None and child.name != scenario:
            continue
        md_path = child / "scenario.md"
        if md_path.exists():
            yield ScenarioSource(
                md_path=md_path,
                yml_path=child / "scenario.yml",
            )


def discover_flat_layout(
    root: pathlib.Path,
    scenario: str | None = None,
) -> Iterable[ScenarioSource]:
    """Discover scenarios using the flat-file layout.

    If `scenario` is given, restrict discovery to the file whose stem
    matches it exactly.
    """
    for md_path in root.glob("*.md"):
        if md_path.name in {"README.md", "scenario_template.md"}:
            continue
        if scenario is not None and md_path.stem != scenario:
            continue
        yield ScenarioSource(
            md_path=md_path,
            yml_path=md_path.with_suffix(".yml"),
        )


def discover_scenarios(
    root: pathlib.Path,
    layout: str,
    scenario: str | None = None,
) -> list[ScenarioSource]:
    if layout == "directory":
        return list(discover_directory_layout(root, scenario=scenario))
    if layout == "flat":
        return list(discover_flat_layout(root, scenario=scenario))
    raise ValueError(f"Unknown scenario layout: {layout}")


# -----------------------------------------------------------------------------
# Distillation
# -----------------------------------------------------------------------------


def distill_scenario(
    source: ScenarioSource,
    *,
    schema_path: pathlib.Path,
    dry_run: bool,
    show_diffs: bool,
) -> None:
    """Distill a single scenario."""

    compiled = compiler.compile_file(
        md_path=source.md_path,
        schema_path=schema_path,
        root_key=DEFAULT_ROOT_KEY,
    )

    yaml_text = utils.dump_yaml(compiled)

    utils.atomic_write(
        path=source.yml_path,
        content=yaml_text,
        dry_run=dry_run,
        show_diffs=show_diffs,
    )


# -----------------------------------------------------------------------------
# High-level entry point
# -----------------------------------------------------------------------------


def distill_all(
    *,
    root: pathlib.Path,
    layout: str = "directory",
    dry_run: bool = False,
    show_diffs: bool = False,
    scenario: str | None = None,
) -> None:
    schema_path = SCHEMA_PATH

    sources = discover_scenarios(root, layout, scenario=scenario)
    if not sources:
        from prosoc.literate.errors import LiterateDiscoveryError

        if scenario is not None:
            raise LiterateDiscoveryError(f"No scenario '{scenario}' found under {root}")
        raise LiterateDiscoveryError(f"No scenarios found under {root}")

    for source in sources:
        distill_scenario(
            source,
            schema_path=schema_path,
            dry_run=dry_run,
            show_diffs=show_diffs,
        )


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Distill social navigation scenarios")
    parser.add_argument(
        "--layout",
        choices=["directory", "flat"],
        default="directory",
        help="Scenario layout style",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show-diffs", action="store_true")
    parser.add_argument(
        "--scenario",
        metavar="ID",
        default=None,
        help="Restrict to a single scenario by directory/id name",
    )

    args = parser.parse_args()

    root = pathlib.Path(__file__).parent

    distill_all(
        root=root,
        layout=args.layout,
        dry_run=args.dry_run,
        show_diffs=args.show_diffs,
        scenario=args.scenario,
    )


if __name__ == "__main__":
    main()
