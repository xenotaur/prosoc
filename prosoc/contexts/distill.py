"""
Context distillation tool.

This module distills human-authored context cards written in
Markdown with fenced YAML blocks into machine-readable YAML files,
validated against the context JSON schema.

Directory layout (default):

prosoc/contexts/<context_id>/context.md -> context.yml

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
DEFAULT_ROOT_KEY = None  # keep consistent with scenarios


# -----------------------------------------------------------------------------
# Context source abstraction
# -----------------------------------------------------------------------------


class ContextSource(NamedTuple):
    md_path: pathlib.Path
    yml_path: pathlib.Path


# -----------------------------------------------------------------------------
# Discovery
# -----------------------------------------------------------------------------


def discover_contexts(root: pathlib.Path) -> Iterable[ContextSource]:
    """Discover contexts using the directory-based layout."""
    for child in root.iterdir():
        if not child.is_dir():
            continue

        md_path = child / "context.md"
        if md_path.exists():
            yield ContextSource(
                md_path=md_path,
                yml_path=child / "context.yml",
            )


# -----------------------------------------------------------------------------
# Distillation
# -----------------------------------------------------------------------------


def distill_context(
    source: ContextSource,
    *,
    schema_path: pathlib.Path,
    dry_run: bool,
    show_diffs: bool,
) -> None:
    """Distill a single context card."""

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
    dry_run: bool = False,
    show_diffs: bool = False,
) -> None:
    schema_path = SCHEMA_PATH

    sources = list(discover_contexts(root))
    if not sources:
        from prosoc.literate.errors import LiterateDiscoveryError

        raise LiterateDiscoveryError(f"No contexts found under {root}")

    for source in sources:
        distill_context(
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
        description="Distill prosocial navigation context cards"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show-diffs", action="store_true")

    args = parser.parse_args()

    root = pathlib.Path(__file__).parent

    distill_all(
        root=root,
        dry_run=args.dry_run,
        show_diffs=args.show_diffs,
    )


if __name__ == "__main__":
    main()
