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
from pathlib import Path

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

ROOT_KEY = "principles"


# ---------------------------------------------------------------------
# Distillation logic
# ---------------------------------------------------------------------


def distill_charter(
    *,
    md_path: Path = DEFAULT_CHARTER_MD,
    schema_path: Path = DEFAULT_SCHEMA_JSON,
) -> dict:
    """
    Compile the charter Markdown into a validated dictionary.

    Raises:
        LiterateError on failure.
    """
    return compiler.compile_file(
        md_path,
        schema_path=schema_path,
        root_key=ROOT_KEY,
    )


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
