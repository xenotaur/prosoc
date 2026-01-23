"""
Distiller for Prosoc Constitution Cards.

Extracts and validates constitution YAML blocks from Markdown files and
emits machine-consumable constitution artifacts.
"""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List

from jsonschema import validate, ValidationError

from prosoc.literate.compiler import (
    load_markdown,
    extract_yaml_blocks,
)
from prosoc.literate.errors import DistillationError
from prosoc.literate.utils import atomic_write


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

CONSTITUTIONS_DIR = Path(__file__).parent
SCHEMA_PATH = CONSTITUTIONS_DIR / "schema.json"
OUTPUT_DIR = CONSTITUTIONS_DIR / "distilled"


# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------

def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _load_schema() -> Dict[str, Any]:
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------
# Core distillation
# ---------------------------------------------------------------------

def distill_constitution(md_path: Path) -> Dict[str, Any]:
    """
    Distill a single constitution Markdown file.

    Returns a validated constitution dictionary with provenance metadata.
    """
    text = load_markdown(md_path)
    yaml_blocks = extract_yaml_blocks(text)

    if len(yaml_blocks) == 0:
        raise DistillationError(
            f"No YAML block found in constitution: {md_path}"
        )
    if len(yaml_blocks) > 1:
        raise DistillationError(
            f"Multiple YAML blocks found in constitution: {md_path}"
        )

    document = yaml_blocks[0]

    if "constitution" not in document:
        raise DistillationError(
            f"Top-level key 'constitution' missing in {md_path}"
        )

    schema = _load_schema()

    try:
        validate(instance=document, schema=schema)
    except ValidationError as e:
        raise DistillationError(
            f"Schema validation failed for {md_path}:\n{e}"
        )

    constitution = document["constitution"]

    # Inject distillation metadata
    constitution["_meta"] = {
        "source_file": str(md_path),
        "source_hash": _hash_text(text),
        "distilled_from": "constitution_card",
    }

    return constitution


# ---------------------------------------------------------------------
# Batch distillation
# ---------------------------------------------------------------------

def distill_all(
    input_dir: Path | None = None,
    output_dir: Path | None = None,
) -> List[Dict[str, Any]]:
    """
    Distill all constitution cards in a directory.
    """
    input_dir = input_dir or CONSTITUTIONS_DIR
    output_dir = output_dir or OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []

    for md_path in sorted(input_dir.glob("*.md")):
        constitution = distill_constitution(md_path)
        cid = constitution["id"]

        out_path = output_dir / f"{cid}.json"
        atomic_write(out_path, json.dumps(constitution, indent=2))

        results.append(constitution)

    # Write index
    index = {
        "count": len(results),
        "constitutions": [
            {
                "id": c["id"],
                "name": c["name"],
                "source_file": c["_meta"]["source_file"],
            }
            for c in results
        ],
    }

    atomic_write(
        output_dir / "index.json",
        json.dumps(index, indent=2),
    )

    return results


# ---------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------

def main() -> None:
    distill_all()


if __name__ == "__main__":
    main()
