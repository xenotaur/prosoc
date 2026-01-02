"""
utils.py

Utility functions for literate compilation workflows.

This module provides:
- Canonical YAML serialization
- Atomic file writes
- Unified diffs for dry-run and review workflows

This module intentionally does NOT:
- Perform compilation or validation
- Know about domains (charter, scenarios, etc.)
"""

from __future__ import annotations

import difflib
import tempfile
from pathlib import Path
from typing import Any

import yaml

from prosoc.literate import errors


# ---------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------


def dump_yaml(data: Any) -> str:
    """
    Serialize Python data to a canonical YAML string.

    This function centralizes YAML formatting decisions so that
    diffs are stable and predictable.

    Args:
        data: Python data to serialize.

    Returns:
        A canonical YAML string.

    Raises:
        LiterateIOError: if serialization fails.
    """
    try:
        return yaml.safe_dump(
            data,
            sort_keys=False,
            default_flow_style=False,
        )
    except yaml.YAMLError as e:
        raise errors.LiterateIOError(
            "Failed to serialize data to YAML"
        ) from e


# ---------------------------------------------------------------------
# Diffing
# ---------------------------------------------------------------------


def unified_diff(
    *,
    old_text: str,
    new_text: str,
    fromfile: str = "before",
    tofile: str = "after",
) -> str:
    """
    Produce a unified diff between two strings.

    Args:
        old_text: Original text.
        new_text: New text.
        fromfile: Name of the original file (default: "before").
        tofile: Name of the new file (default: "after").

    Returns:
        A unified diff string.
    """
    diff = difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=fromfile,
        tofile=tofile,
    )
    return "".join(diff)


# ---------------------------------------------------------------------
# Atomic file writes
# ---------------------------------------------------------------------


def atomic_write(
    path: Path,
    content: str,
    *,
    encoding: str = "utf-8",
) -> None:
    """
    Atomically write content to a file.

    The file is written to a temporary location and then
    replaced to avoid partial writes.

    Args:
        path: Path to the file to write.
        content: Content to write to the file.
        encoding: Encoding to use for writing the file (default: "utf-8").

    Raises:
        LiterateIOError on failure.
    """
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding=encoding,
            delete=False,
            dir=path.parent,
        ) as tmp:
            tmp.write(content)
            temp_path = Path(tmp.name)

        temp_path.replace(path)

    except OSError as e:
        raise errors.LiterateIOError(
            f"Failed to atomically write file: {path}"
        ) from e
