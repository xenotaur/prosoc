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
``scripts/validate/status`` (via ``prosoc.nca.utils.cards.validate_status``) is the
CLI wrapper that applies these checks per family, and its ``--fix`` mode
projects the authoritative YAML ``state`` back onto the Markdown ``STATE`` line.

Two additional, independent checks live here too: :func:`check_audit_evidence`
(does an ``AUDITED``/``APPROVED`` card have a sibling ``audit.md`` with a
``ready``/``ready_with_fixes`` verdict — the real signal, not the optional
``AUDITED:`` provenance bullet) and :func:`check_charter_status_line`
(charter-only: does the charter's free-text ``**Status:**`` header agree with
its ``STATE``). Neither is addressed by ``--fix``, which only ever projects
the YAML ``state`` onto the Markdown ``STATE`` line.

The canonical state vocabulary is defined here and mirrored by each family's
``schema.json`` and by ``src/prosoc/prnc/scenarios/workflow.md`` (the lifecycle
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
# ``- **STATE:** DRAFTED``. The ``prefix`` and ``suffix`` groups capture the
# surrounding text (including any trailing whitespace used for Markdown line
# breaks) so projection can swap only the state token and leave the rest intact.
# ``[^\S\n]`` is horizontal whitespace only, so ``$`` still anchors to line end.
_STATE_LINE_RE = re.compile(
    r"^(?P<prefix>- \*\*STATE:\*\*[^\S\n]*)(?P<state>\S+)(?P<suffix>[^\S\n]*)$",
    re.MULTILINE,
)


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
    # Swap only the state token; keep the prefix and any trailing whitespace
    # (e.g. the two trailing spaces task cards use for Markdown line breaks).
    return _STATE_LINE_RE.sub(
        lambda m: m.group("prefix") + state + m.group("suffix"), md_text, count=1
    )


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
# File-level helpers (used by prosoc.nca.utils.cards.validate_status)
# -----------------------------------------------------------------------------


def read_yaml_state(yml_path: pathlib.Path, root_key: str | None = None) -> str:
    """Return the ``state`` field from a distilled card ``*.yml``.

    Most families keep ``state`` at the top level. Root-wrapped families (e.g.
    constitutions, whose payload nests under a ``constitution:`` key) pass
    ``root_key`` so the state is read from ``data[root_key]["state"]``.

    Raises:
        StatusStateError: if the expected ``state`` field is absent.
    """
    data = yaml.safe_load(yml_path.read_text(encoding="utf-8"))
    if root_key is not None:
        if not isinstance(data, dict) or not isinstance(data.get(root_key), dict):
            raise StatusStateError(f"{yml_path} has no '{root_key}' mapping")
        data = data[root_key]
        where = f"'{root_key}.state'"
    else:
        where = "top-level 'state'"
    if not isinstance(data, dict) or "state" not in data:
        raise StatusStateError(f"{yml_path} has no {where} field")
    return str(data["state"])


def check_source(
    md_path: pathlib.Path, yml_path: pathlib.Path, root_key: str | None = None
) -> ConsistencyResult:
    """Check that a card's Markdown STATE line and YAML ``state`` agree.

    ``root_key`` is forwarded to :func:`read_yaml_state` for root-wrapped
    families (see its docstring).
    """
    markdown_state = parse_markdown_state(md_path.read_text(encoding="utf-8"))
    yaml_state = read_yaml_state(yml_path, root_key=root_key)
    return check_consistency(markdown_state=markdown_state, yaml_state=yaml_state)


# -----------------------------------------------------------------------------
# Audit-evidence check: does an AUDITED/APPROVED card actually have a sibling
# ``audit.md`` with an acceptable verdict? (used by
# prosoc.nca.utils.cards.validate_status)
# -----------------------------------------------------------------------------

# Frontmatter-only verdicts that constitute acceptable audit evidence for an
# AUDITED/APPROVED card. "blocking" or any other verdict is not acceptable.
_ACCEPTABLE_AUDIT_VERDICTS = ("ready", "ready_with_fixes")

# ``audit.md``'s leading YAML frontmatter block (``---`` ... ``---``).
_FRONTMATTER_RE = re.compile(r"\A---\n(?P<yaml>.*?)\n---", re.DOTALL)


def read_audit_verdict(audit_path: pathlib.Path) -> str | None:
    """Return the ``verdict:`` value from an ``audit.md``'s frontmatter.

    Returns ``None`` if the file has no parseable frontmatter or no
    ``verdict`` key — the caller treats that the same as a missing file.
    """
    match = _FRONTMATTER_RE.match(audit_path.read_text(encoding="utf-8"))
    if match is None:
        return None
    data = yaml.safe_load(match.group("yaml"))
    if not isinstance(data, dict) or "verdict" not in data:
        return None
    return str(data["verdict"])


def check_audit_evidence(md_path: pathlib.Path, state: str) -> ConsistencyResult:
    """Check that a card at ``AUDITED``/``APPROVED`` has real audit evidence.

    The optional ``- **AUDITED:**`` provenance bullet in a card's
    ``## Status`` block is *not* evidence (``workflow.md`` makes it an
    optional addition to the history, not a required field) — the real
    signal is a sibling ``audit.md`` (next to ``md_path``) with a verdict
    of ``ready`` or ``ready_with_fixes``. Cards below ``AUDITED`` have
    nothing to check here.
    """
    if state not in ("AUDITED", "APPROVED"):
        return ConsistencyResult(True, f"audit evidence not required at {state}")
    audit_path = md_path.parent / "audit.md"
    if not audit_path.exists():
        return ConsistencyResult(
            False, f"{state} card has no sibling audit.md at {audit_path}"
        )
    verdict = read_audit_verdict(audit_path)
    if verdict not in _ACCEPTABLE_AUDIT_VERDICTS:
        return ConsistencyResult(
            False,
            f"{audit_path} has no acceptable verdict for {state} "
            f"(found {verdict!r}, need one of {_ACCEPTABLE_AUDIT_VERDICTS})",
        )
    return ConsistencyResult(
        True, f"audit.md verdict {verdict!r} acceptable for {state}"
    )


# -----------------------------------------------------------------------------
# Charter-only check: does the free-text ``**Status:**`` header line (a
# separate field from the ``## Status`` block's ``**STATE:**`` bullet) agree
# with the authoritative state? Only the charter has this redundant field.
# -----------------------------------------------------------------------------

_CHARTER_STATUS_LINE_RE = re.compile(
    r"^\*\*Status:\*\*[^\S\n]*(?P<value>[^\n]+?)[^\S\n]*$", re.MULTILINE
)

# The free-text header's human-friendly label sometimes differs from the
# STATE token itself — observed convention: "Draft (Normative)" for
# DRAFTED, not "Drafted". Every other state's label is just its lowercased
# token (e.g. "approved" for APPROVED), which is what's actually exercised
# in the real corpus today.
_STATUS_LINE_LABELS: dict[str, str] = {"DRAFTED": "draft"}


def parse_charter_status_line(md_text: str) -> str | None:
    """Return the free-text value of the charter's top-level ``**Status:**``
    line, or ``None`` if the line isn't present (nothing to check)."""
    match = _CHARTER_STATUS_LINE_RE.search(md_text)
    return match.group("value") if match is not None else None


def check_charter_status_line(md_text: str, state: str) -> ConsistencyResult:
    """Check the charter's free-text ``**Status:**`` line against ``state``.

    Case-insensitive substring match against the state's human-friendly
    label (see :data:`_STATUS_LINE_LABELS`) — the field is free text, not a
    controlled vocabulary, so this isn't a vocabulary-exact comparison. A
    card with no such line (any non-charter family) has nothing to check.
    """
    value = parse_charter_status_line(md_text)
    if value is None:
        return ConsistencyResult(True, "no free-text Status: line present")
    label = _STATUS_LINE_LABELS.get(state, state.lower())
    if label not in value.lower():
        return ConsistencyResult(
            False, f"free-text Status: {value!r} does not reflect STATE {state!r}"
        )
    return ConsistencyResult(
        True, f"free-text Status: {value!r} matches STATE {state!r}"
    )
