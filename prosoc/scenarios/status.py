"""
Scenario lifecycle-state helpers.

A scenario's lifecycle state is recorded in two places that must agree:

1. the machine-readable ``state`` field of its embedded (fenced) YAML — the
   authoritative source, distilled into ``scenario.yml``; and
2. the ``- **STATE:**`` line of its human-readable ``## Status`` Markdown block,
   which is a projection of (1).

This module provides pure helpers to parse the Markdown ``STATE`` line, to
project a state value back into the Markdown, and to check that the two
representations agree. ``scripts/validate/status`` is the CLI wrapper: it
reports disagreements by default, and its ``--fix`` mode projects the
authoritative YAML ``state`` back onto the Markdown ``STATE`` line.

The canonical state vocabulary is defined here and mirrored by
``prosoc/scenarios/schema.json`` and ``prosoc/scenarios/workflow.md``.
"""

from __future__ import annotations

import pathlib
import re
from typing import NamedTuple

import yaml

# Canonical lifecycle states a scenario card can be in. ``SOURCE`` is a
# provenance stage, not a ``state`` value (see workflow.md). Keep this in sync
# with the ``state`` enum in schema.json.
STATES: tuple[str, ...] = (
    "DRAFTED",
    "EDITED",
    "AUDITED",
    "APPROVED",
    "VALIDATED",
    "DEPRECATED",
    "RETIRED",
)

# The authoritative STATE line inside a ``## Status`` block, e.g.
# ``- **STATE:** DRAFTED``.
_STATE_LINE_RE = re.compile(r"^- \*\*STATE:\*\*\s*(?P<state>\S+)\s*$", re.MULTILINE)


class StatusStateError(ValueError):
    """Raised when a scenario's Markdown STATE line is missing or malformed."""


def parse_markdown_state(md_text: str) -> str:
    """Return the ``STATE`` value from a scenario.md ``## Status`` block.

    Raises:
        StatusStateError: if no ``- **STATE:**`` line is present.
    """
    match = _STATE_LINE_RE.search(md_text)
    if match is None:
        raise StatusStateError("no '- **STATE:**' line found in Markdown")
    return match.group("state")


def project_state_into_markdown(md_text: str, state: str) -> str:
    """Return ``md_text`` with its ``- **STATE:**`` line set to ``state``.

    The Markdown STATE line is a projection of the authoritative YAML ``state``;
    this rewrites it to match. Idempotent when the line already agrees.

    Raises:
        StatusStateError: if no ``- **STATE:**`` line is present to project onto.
        ValueError: if ``state`` is not a recognised lifecycle state.
    """
    if state not in STATES:
        raise ValueError(f"unrecognised lifecycle state: {state!r}")
    if _STATE_LINE_RE.search(md_text) is None:
        raise StatusStateError("no '- **STATE:**' line found to project onto")
    return _STATE_LINE_RE.sub(f"- **STATE:** {state}", md_text, count=1)


class ConsistencyResult(NamedTuple):
    ok: bool
    detail: str


def check_consistency(*, markdown_state: str, yaml_state: str) -> ConsistencyResult:
    """Check that the Markdown STATE line agrees with the YAML ``state`` field.

    Both values must be recognised states and must be equal.
    """
    problems: list[str] = []
    if yaml_state not in STATES:
        problems.append(f"YAML state {yaml_state!r} is not a recognised state")
    if markdown_state not in STATES:
        problems.append(f"Markdown STATE {markdown_state!r} is not a recognised state")
    if markdown_state != yaml_state:
        problems.append(
            f"Markdown STATE ({markdown_state!r}) != YAML state ({yaml_state!r})"
        )
    if problems:
        return ConsistencyResult(False, "; ".join(problems))
    return ConsistencyResult(True, f"state {yaml_state} consistent")


# -----------------------------------------------------------------------------
# File-level helpers (used by scripts/validate/status)
# -----------------------------------------------------------------------------


def read_yaml_state(yml_path: pathlib.Path) -> str:
    """Return the ``state`` field from a distilled ``scenario.yml``.

    Raises:
        StatusStateError: if the file has no top-level ``state`` field.
    """
    data = yaml.safe_load(yml_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "state" not in data:
        raise StatusStateError(f"{yml_path} has no top-level 'state' field")
    return str(data["state"])


def check_source(md_path: pathlib.Path, yml_path: pathlib.Path) -> ConsistencyResult:
    """Check that a scenario's Markdown STATE line and YAML ``state`` agree."""
    markdown_state = parse_markdown_state(md_path.read_text(encoding="utf-8"))
    yaml_state = read_yaml_state(yml_path)
    return check_consistency(markdown_state=markdown_state, yaml_state=yaml_state)
