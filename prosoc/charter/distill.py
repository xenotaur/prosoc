"""
distill.py

Compiler-style tool that distills a literate charter.md into a
machine-readable charter.yml.

This module:
- Extracts fenced YAML blocks from Markdown
- Parses them into Python objects
- Validates against a JSON Schema
- Emits a canonical charter dictionary

This module intentionally does NOT:
- Define runtime behavior
- Use Pydantic
- Apply domain semantics
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List, Dict, Any

import yaml
from jsonschema import validate as jsonschema_validate, ValidationError as SchemaValidationError


# ---------------------------------------------------------------------
# Constants and defaults
# ---------------------------------------------------------------------

DEFAULT_CHARTER_MD = Path(__file__).parent / "charter.md"
DEFAULT_CHARTER_YAML = Path(__file__).parent / "charter.yml"
DEFAULT_SCHEMA_JSON = Path(__file__).parent / "schema.json"

YAML_FENCE_LANGUAGE = "yaml"

_YAML_BLOCK_RE = re.compile(
    rf"```{YAML_FENCE_LANGUAGE}\s+(.*?)\s+```",
    re.DOTALL | re.IGNORECASE,
)


# ---------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------

def extract_yaml_blocks(markdown_text: str) -> List[str]:
    """
    Extract all fenced ```yaml blocks from a Markdown document.

    Args:
        markdown_text: Full Markdown document as a string.

    Returns:
        List of raw YAML strings (without fences).

    Raises:
        ValueError: if no YAML blocks are found.
    """
    blocks = _YAML_BLOCK_RE.findall(markdown_text)
    if not blocks:
        raise ValueError("No fenced YAML blocks found in charter.md")
    return blocks


# ---------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------

def parse_yaml_blocks(blocks: List[str]) -> List[Dict[str, Any]]:
    """
    Parse raw YAML blocks into Python dictionaries.

    Args:
        blocks: List of raw YAML strings.

    Returns:
        List of parsed YAML objects (one per principle).

    Raises:
        ValueError: if any block fails to parse.
    """
    principles: List[Dict[str, Any]] = []

    for i, block in enumerate(blocks):
        try:
            parsed = yaml.safe_load(block)
        except yaml.YAMLError as e:
            raise ValueError(
                f"Failed to parse YAML block #{i + 1}"
            ) from e

        if not isinstance(parsed, dict):
            raise ValueError(
                f"YAML block #{i + 1} did not parse to a mapping/object"
            )

        principles.append(parsed)

    return principles


# ---------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------

def assemble_charter(principles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Assemble the top-level charter structure.

    Args:
        principles: List of principle dictionaries.

    Returns:
        Charter dictionary suitable for schema validation.
    """
    return {
        "principles": principles
    }


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

def validate_charter(charter: Dict[str, Any], schema: Dict[str, Any]) -> None:
    """
    Validate a charter dictionary against the JSON Schema.

    Args:
        charter: Parsed charter dictionary.
        schema: Loaded JSON Schema.

    Raises:
        SchemaValidationError: if validation fails.
    """
    jsonschema_validate(instance=charter, schema=schema)


# ---------------------------------------------------------------------
# High-level pipeline
# ---------------------------------------------------------------------

def distill_markdown_to_yaml(
    markdown_text: str,
    schema: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Full distillation pipeline from Markdown text to validated charter dict.

    Args:
        markdown_text: Charter Markdown source.
        schema: JSON Schema dictionary.

    Returns:
        Validated charter dictionary.

    Raises:
        ValueError, SchemaValidationError on failure.
    """
    blocks = extract_yaml_blocks(markdown_text)
    principles = parse_yaml_blocks(blocks)
    charter = assemble_charter(principles)
    validate_charter(charter, schema)
    return charter


def distill_file(
    md_path: Path = DEFAULT_CHARTER_MD,
    schema_path: Path = DEFAULT_SCHEMA_JSON,
) -> Dict[str, Any]:
    """
    Distill a charter.md file into a validated charter dictionary.

    Args:
        md_path: Path to charter.md.
        schema_path: Path to charter.schema.json.

    Returns:
        Validated charter dictionary.
    """
    markdown_text = md_path.read_text(encoding="utf-8")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return distill_markdown_to_yaml(markdown_text, schema)


# ---------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------

def main() -> None:
    """
    CLI entry point: distill charter.md → charter.yml
    """
    charter = distill_file()

    with open(DEFAULT_CHARTER_YAML, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            charter,
            f,
            sort_keys=False,
            default_flow_style=False,
        )

    print(f"Wrote distilled charter to {DEFAULT_CHARTER_YAML}")


if __name__ == "__main__":
    main()
