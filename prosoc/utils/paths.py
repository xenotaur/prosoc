"""
Path utilities for locating important project roots.

This module is intentionally small and dependency-free.
"""

from __future__ import annotations

from pathlib import Path


class RepoRootNotFoundError(RuntimeError):
    """Raised when the repository root cannot be located."""


def find_repo_root(
    start: Path | None = None,
    *,
    marker_files: tuple[str, ...] = ("pyproject.toml",),
    max_depth: int = 10,
) -> Path:
    """
    Find the Prosoc repository root by walking upward from a starting path.

    The repository root is identified by the presence of one or more
    marker files (default: 'pyproject.toml').

    Parameters
    ----------
    start : pathlib.Path, optional
        Path to start searching from. Defaults to this file's location.
    marker_files : tuple of str
        Filenames whose presence indicates the repository root.
    max_depth : int
        Maximum number of parent directories to search.

    Returns
    -------
    pathlib.Path
        Path to the repository root.

    Raises
    ------
    RepoRootNotFoundError
        If no repository root is found within max_depth.
    """

    if start is None:
        start = Path(__file__).resolve()

    current = start if start.is_dir() else start.parent

    for _ in range(max_depth):
        if any((current / marker).exists() for marker in marker_files):
            return current
        if current.parent == current:
            break
        current = current.parent

    raise RepoRootNotFoundError(
        f"Could not find repository root containing {marker_files} "
        f"starting from {start}"
    )
