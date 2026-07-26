"""
Card lifecycle-state helpers (family-agnostic).

Every prosoc normative card records its lifecycle state in two places that must
agree:

1. the machine-readable ``state`` field of its embedded (fenced) YAML — the
   authoritative source, distilled into the card's ``*.yml``; and
2. the ``- **STATE:**`` line of its human-readable ``## Status`` / ``## STATUS``
   Markdown block, which is a projection of (1).

This module provides pure helpers to parse the Markdown ``STATE`` line, to
project a state value back into the Markdown, and to check that the two
representations agree. It is shared across card families (scenarios, tasks, …);
``scripts/validate/status`` (via ``prosoc.utils.cards.validate_status``) is the
CLI wrapper that applies these checks per family, and its ``--fix`` mode
projects the authoritative YAML ``state`` back onto the Markdown ``STATE`` line.

The canonical state vocabulary is defined here and mirrored by each family's
``schema.json`` and by ``prosoc/scenarios/workflow.md`` (the lifecycle
definition of record).
"""

from __future__ import annotations

import pathlib
import re
from typing import NamedTuple

import yaml

# Canonical lifecycle states a card can be in. ``SOURCE`` is a provenance stage,
# not a ``state`` value (see workflow.md). Keep this in sync with the ``state``
# enum in each family's schema.json.
STATES: tuple[str, ...] = (
    "DRAFTED",
    "EDITED",
    "AUDITED",
    "APPROVED",
    "VALIDATED",
    "DEPRECATED",
    "RETIRED",
)

# The authoritative STATE line inside a ``## Status`` / ``## STATUS`` block, e.g.
# ``- **STATE:** DRAFTED``. Tolerates trailing whitespace (Markdown line breaks).
_STATE_LINE_RE = re.compile(r"^- \*\*STATE:\*\*\s*(?P<state>\S+)\s*$", re.MULTILINE)


class StatusStateError(ValueError):
    """Raised when a card's Markdown STATE line is missing or malformed."""


def parse_markdown_state(md_text: str) -> str:
    """Return the ``STATE`` value from a card's ``## Status`` block.

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
# File-level helpers (used by prosoc.utils.cards.validate_status)
# -----------------------------------------------------------------------------


def read_yaml_state(yml_path: pathlib.Path) -> str:
    """Return the ``state`` field from a distilled card ``*.yml``.

    Raises:
        StatusStateError: if the file has no top-level ``state`` field.
    """
    data = yaml.safe_load(yml_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "state" not in data:
        raise StatusStateError(f"{yml_path} has no top-level 'state' field")
    return str(data["state"])


def check_source(md_path: pathlib.Path, yml_path: pathlib.Path) -> ConsistencyResult:
    """Check that a card's Markdown STATE line and YAML ``state`` agree."""
    markdown_state = parse_markdown_state(md_path.read_text(encoding="utf-8"))
    yaml_state = read_yaml_state(yml_path)
    return check_consistency(markdown_state=markdown_state, yaml_state=yaml_state)
