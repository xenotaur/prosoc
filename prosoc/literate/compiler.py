"""Generic compiler for literate Markdown artifacts.

This module:
- Extracts fenced YAML blocks from Markdown
- Parses them into Python objects
- Validates against a JSON Schema
- Returns a canonical Python dictionary

This module intentionally does NOT:
- Know about domains (charter, scenarios, robots, etc.)
- Define runtime behavior
- Perform I/O unless explicitly requested
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

import yaml
import jsonschema

from prosoc.literate import errors


YAML_FENCE_LANGUAGE = "yaml"

_YAML_BLOCK_RE = re.compile(
    rf"```{YAML_FENCE_LANGUAGE}\s+(.*?)\s+```",
    re.DOTALL | re.IGNORECASE,
)

# ---------------------------------------------------------------------
# Core compilation steps
# ---------------------------------------------------------------------


def extract_yaml_blocks(markdown_text: str) -> List[str]:
    """
    Extract all fenced YAML blocks from a Markdown document.

    Args:
        markdown_text: Markdown source text.

    Returns:
        List of yaml blocks found in the markdown text.

    Raises:
        LiterateSourceError: if no YAML blocks are found.
    """
    blocks = _YAML_BLOCK_RE.findall(markdown_text)
    if not blocks:
        raise errors.LiterateSourceError(
            "No fenced YAML blocks found in Markdown source"
        )
    return blocks


def parse_yaml_blocks(blocks: List[str]) -> List[Dict[str, Any]]:
    """
    Parse raw YAML blocks into Python dictionaries.

    Args:
        blocks: List of raw YAML blocks.

    Returns:
        List of parsed YAML blocks.

    Raises:
        LiterateYamlError: if YAML parsing fails.
        LiterateStructureError: if parsed YAML is not a mapping.
    """
    parsed_blocks: List[Dict[str, Any]] = []

    for i, block in enumerate(blocks):
        try:
            parsed = yaml.safe_load(block)
        except yaml.YAMLError as e:
            raise errors.LiterateYamlError(
                f"Failed to parse YAML block #{i + 1}"
            ) from e

        if not isinstance(parsed, dict):
            raise errors.LiterateStructureError(
                f"YAML block #{i + 1} did not parse to a mapping/object"
            )

        parsed_blocks.append(parsed)

    return parsed_blocks


def assemble_document(
    items: List[Dict[str, Any]],
    *,
    root_key: str,
) -> Dict[str, Any]:
    """
    Assemble parsed YAML blocks into a top-level document.

    Args:
        items: List of parsed YAML blocks.
        root_key: Key to use for the root of the document.

    Returns:
        A document dictionary with the root_key as the top-level key.

    Raises:
        LiterateStructureError: if root_key is invalid.
    """
    if not root_key or not isinstance(root_key, str):
        raise errors.LiterateStructureError(
            "root_key must be a non-empty string"
        )

    return {root_key: items}


def validate_document(
    document: Dict[str, Any],
    schema: Dict[str, Any],
) -> None:
    """
    Validate a document against a JSON Schema.

    Args:
        document: Document to validate.
        schema: JSON Schema to validate against.

    Raises:
        LiterateSchemaError: if validation fails.
    """
    try:
        jsonschema.validate(instance=document, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise errors.LiterateSchemaError(
            "Document failed schema validation"
        ) from e


# ---------------------------------------------------------------------
# High-level API (pure functions)
# ---------------------------------------------------------------------


def compile_markdown(
    markdown_text: str,
    *,
    schema: Dict[str, Any],
    root_key: str,
) -> Dict[str, Any]:
    """
    Compile Markdown source into a validated document dictionary.

    Args:
        markdown_text: Markdown source text.
        schema: JSON Schema to validate against.
        root_key: Key to use for the root of the document.

    Returns:
        A validated document dictionary.

    Raises:
        LiterateSourceError: if no YAML blocks are found.
        LiterateYamlError: if YAML parsing fails.
        LiterateStructureError: if parsed YAML is not a mapping.
        LiterateSchemaError: if document fails schema validation.
    """
    blocks = extract_yaml_blocks(markdown_text)
    items = parse_yaml_blocks(blocks)
    document = assemble_document(items, root_key=root_key)
    validate_document(document, schema)
    return document


def compile_file(
    md_path: Path,
    *,
    schema_path: Path,
    root_key: str,
) -> Dict[str, Any]:
    """
    Compile a Markdown file into a validated document dictionary.

    Args:
        md_path: Path to the Markdown file.
        schema_path: Path to the JSON Schema file.
        root_key: Key to use for the root of the document.

    Returns:
        A validated document dictionary.

    Raises:
        LiterateIOError: if files cannot be read.
    """
    try:
        markdown_text = md_path.read_text(encoding="utf-8")
    except OSError as e:
        raise errors.LiterateIOError(
            f"Failed to read Markdown file: {md_path}"
        ) from e

    try:
        schema_text = schema_path.read_text(encoding="utf-8")
        schema = json.loads(schema_text)
    except (OSError, json.JSONDecodeError) as e:
        raise errors.LiterateIOError(
            f"Failed to read or parse schema file: {schema_path}"
        ) from e

    return compile_markdown(
        markdown_text,
        schema=schema,
        root_key=root_key,
    )
