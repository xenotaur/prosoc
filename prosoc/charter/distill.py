"""
distill.py

Charter-specific distillation tool.

Compiles `charter.md` into a validated, machine-readable `charter.yml`.

Supports:
- --dry-run     (do not write output)
- --show-diffs  (display unified diff of changes)

This module adapts the generic literate compiler to the
Prosocial Navigation Charter.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, NamedTuple

from prosoc.literate import compiler
from prosoc.literate import errors
from prosoc.literate import utils


# ---------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------

CHARTER_DIR = Path(__file__).parent

DEFAULT_CHARTER_MD = CHARTER_DIR / "charter.md"
DEFAULT_SCHEMA_JSON = CHARTER_DIR / "schema.json"
DEFAULT_CHARTER_YML = CHARTER_DIR / "charter.yml"

STATE_KEY = "state"
PRINCIPLES_KEY = "principles"


# ---------------------------------------------------------------------
# Source abstraction (single-source family)
# ---------------------------------------------------------------------


class CharterSource(NamedTuple):
    md_path: Path
    yml_path: Path


def discover_charter(root: Path) -> list[CharterSource]:
    """Discover the single charter source under ``root``.

    The charter is a single document (``charter.md`` -> ``charter.yml``), not a
    directory of cards, so this returns at most one source. Mirrors the
    ``discover_*`` helpers of the card-per-directory families so the status
    validator can register the charter as a single-source family.
    """
    md_path = root / "charter.md"
    if not md_path.exists():
        return []
    return [CharterSource(md_path=md_path, yml_path=root / "charter.yml")]


# ---------------------------------------------------------------------
# Distillation logic
# ---------------------------------------------------------------------


def _split_blocks(blocks: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    """Separate the document-level state block from the principle blocks.

    The charter's fenced YAML blocks are the ten principle blocks (each with an
    ``id``) plus exactly one document-level block carrying the lifecycle
    ``state`` (and no ``id``). The generic ``compiler.assemble_document`` would
    sweep every block into ``principles``; the charter instead needs the state
    lifted to a top-level sibling. Returns ``(state, principle_blocks)``.
    """
    principle_blocks = [b for b in blocks if isinstance(b, dict) and "id" in b]
    state_blocks = [
        b for b in blocks if isinstance(b, dict) and "state" in b and "id" not in b
    ]
    if len(state_blocks) != 1:
        raise errors.LiterateStructureError(
            "Expected exactly one document-level state block (a fenced YAML "
            f"block with 'state' and no 'id'); found {len(state_blocks)}"
        )
    classified = len(principle_blocks) + len(state_blocks)
    if classified != len(blocks):
        raise errors.LiterateStructureError(
            f"{len(blocks) - classified} fenced YAML block(s) were neither a "
            "principle (with 'id') nor the document state block (with 'state')"
        )
    return state_blocks[0]["state"], principle_blocks


def distill_charter(
    *,
    md_path: Path = DEFAULT_CHARTER_MD,
    schema_path: Path = DEFAULT_SCHEMA_JSON,
) -> dict:
    """
    Compile the charter Markdown into a validated dictionary.

    Unlike the generic ``compiler.compile_file`` (which validates mid-compile
    and would sweep every fenced block into ``principles``), the charter carries
    a document-level ``state`` alongside its principles. This separates the
    authoritative state block from the principle blocks, assembles
    ``{state, principles}``, and validates the result against the schema.

    Raises:
        LiterateError on failure.
    """
    try:
        markdown_text = md_path.read_text(encoding="utf-8")
    except OSError as e:
        raise errors.LiterateIOError(f"Failed to read Markdown file: {md_path}") from e

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise errors.LiterateIOError(
            f"Failed to read or parse schema file: {schema_path}"
        ) from e

    blocks = compiler.parse_yaml_blocks(compiler.extract_yaml_blocks(markdown_text))
    state, principle_blocks = _split_blocks(blocks)

    document = {STATE_KEY: state, PRINCIPLES_KEY: principle_blocks}
    compiler.validate_document(document, schema)
    return document


# ---------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Distill charter.md into charter.yml")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write charter.yml; validate and report only",
    )
    parser.add_argument(
        "--show-diffs",
        action="store_true",
        help="Show unified diff between existing and generated charter.yml",
    )

    args = parser.parse_args()

    try:
        charter = distill_charter()
    except errors.LiterateError as e:
        print(f"ERROR: {e}")
        raise SystemExit(1) from e

    new_yaml = utils.dump_yaml(charter)

    if DEFAULT_CHARTER_YML.exists():
        old_yaml = DEFAULT_CHARTER_YML.read_text(encoding="utf-8")
    else:
        old_yaml = ""

    if args.show_diffs:
        diff = utils.unified_diff(
            old_text=old_yaml,
            new_text=new_yaml,
            fromfile=str(DEFAULT_CHARTER_YML),
            tofile=f"{DEFAULT_CHARTER_YML} (generated)",
        )
        if diff:
            print(diff)
        else:
            print("No differences detected.")

    if args.dry_run:
        print("Dry run: charter.yml was not written.")
        return

    if new_yaml != old_yaml:
        try:
            utils.atomic_write(DEFAULT_CHARTER_YML, new_yaml)
        except errors.LiterateIOError as e:
            print(f"ERROR: {e}")
            raise SystemExit(1) from e

        print(f"Wrote distilled charter to {DEFAULT_CHARTER_YML}")
    else:
        print("charter.yml is already up to date.")


if __name__ == "__main__":
    main()
