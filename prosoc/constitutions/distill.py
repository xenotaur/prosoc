"""
Constitution distillation tool.

This module distills human-authored social navigation constitutions written in
Markdown with fenced YAML blocks into machine-readable YAML files, validated
against the constitution JSON schema.

It supports two layouts:

1. Directory layout (default):
   prosoc/constitutions/<constitution_id>/constitution.md -> constitution.yml

2. Flat layout (legacy / optional):
   prosoc/constitutions/<constitution_id>.md -> <constitution_id>.yml

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
DEFAULT_ROOT_KEY = None  # was "constitution"


# -----------------------------------------------------------------------------
# Constitution source abstraction
# -----------------------------------------------------------------------------


class ConstitutionSource(NamedTuple):
    md_path: pathlib.Path
    yml_path: pathlib.Path


# -----------------------------------------------------------------------------
# Discovery
# -----------------------------------------------------------------------------


def discover_directory_layout(root: pathlib.Path) -> Iterable[ConstitutionSource]:
    """Discover constitutions using the directory-based layout."""
    for child in root.iterdir():
        if not child.is_dir():
            continue
        md_path = child / "constitution.md"
        if md_path.exists():
            yield ConstitutionSource(
                md_path=md_path,
                yml_path=child / "constitution.yml",
            )


def discover_flat_layout(root: pathlib.Path) -> Iterable[ConstitutionSource]:
    """Discover constitutions using the flat-file layout."""
    for md_path in root.glob("*.md"):
        if md_path.name in {"README.md", "constitution_template.md"}:
            continue
        yield ConstitutionSource(
            md_path=md_path,
            yml_path=md_path.with_suffix(".yml"),
        )


def discover_constitutions(
    root: pathlib.Path,
    layout: str,
) -> list[ConstitutionSource]:
    if layout == "directory":
        return list(discover_directory_layout(root))
    if layout == "flat":
        return list(discover_flat_layout(root))
    raise ValueError(f"Unknown constitution layout: {layout}")


# -----------------------------------------------------------------------------
# Distillation
# -----------------------------------------------------------------------------


def distill_constitution(
    source: ConstitutionSource,
    *,
    schema_path: pathlib.Path,
    dry_run: bool,
    show_diffs: bool,
) -> None:
    """Distill a single constitution."""

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
) -> None:
    schema_path = SCHEMA_PATH

    sources = discover_constitutions(root, layout)
    if not sources:
        from prosoc.literate.errors import LiterateDiscoveryError

        raise LiterateDiscoveryError(f"No constitutions found under {root}")

    for source in sources:
        distill_constitution(
            source,
            schema_path=schema_path,
            dry_run=dry_run,
            show_diffs=show_diffs,
        )


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Distill social navigation constitutions"
    )
    parser.add_argument(
        "--layout",
        choices=["directory", "flat"],
        default="directory",
        help="Constitution layout style",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show-diffs", action="store_true")

    args = parser.parse_args()

    root = pathlib.Path(__file__).parent

    distill_all(
        root=root,
        layout=args.layout,
        dry_run=args.dry_run,
        show_diffs=args.show_diffs,
    )


if __name__ == "__main__":
    main()
