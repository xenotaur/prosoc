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

Three additional, independent checks live here too: :func:`check_audit_evidence`
(does an ``AUDITED``/``APPROVED`` card have a sibling ``audit.md`` with a
``ready``/``ready_with_fixes`` verdict — the real signal, not the optional
``AUDITED:`` provenance bullet), :func:`check_audit_currency` (has the card's
content drifted since that audit evidence was last touched — comparing
git history with the lifecycle-tracking surface masked out, so an ordinary
promotion or a provenance backfill never false-positives), and
:func:`check_charter_status_line` (charter-only: does the charter's
free-text ``**Status:**`` header agree with its ``STATE``). None of the
three is addressed by ``--fix``, which only ever projects the YAML
``state`` onto the Markdown ``STATE`` line.

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

# A STATUS-block history bullet whose label is a recognised lifecycle state,
# e.g. ``- **AUDITED:** Claude, 2026-08-02``. ``STATES`` is defined above this
# point in the module, so the pattern always reflects the current vocabulary.
_HISTORY_BULLET_RE = re.compile(r"^- \*\*(?:" + "|".join(STATES) + r"):\*\*")


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

    Returns ``None`` if the file has no parseable frontmatter, malformed
    YAML, or no ``verdict`` key — the caller treats all three the same as
    a missing/unacceptable file, never raising. A single malformed
    ``audit.md`` must fail only its own card's check, not abort an entire
    corpus scan.
    """
    match = _FRONTMATTER_RE.match(audit_path.read_text(encoding="utf-8"))
    if match is None:
        return None
    try:
        data = yaml.safe_load(match.group("yaml"))
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict) or "verdict" not in data:
        return None
    return str(data["verdict"])


def audit_path_for(md_path: pathlib.Path, *, layout: str = "directory") -> pathlib.Path:
    """Return the ``audit.md`` path a card at ``md_path`` is checked against.

    In directory layout each card has its own subdirectory, so a sibling
    ``audit.md`` unambiguously belongs to it. In flat layout every card in
    a root shares the same parent directory — a bare sibling ``audit.md``
    would silently "prove" audit evidence for every card in that root, not
    just the one being checked — so flat-layout cards use a card-specific
    ``<stem>.audit.md`` instead, mirroring the ``<stem>.yml`` distillation
    convention already used for flat layout. Shared by
    :func:`check_audit_evidence` and the audit-currency check in
    ``validate_status.py`` so both agree on which file is "the" audit.
    """
    if layout == "flat":
        return md_path.parent / f"{md_path.stem}.audit.md"
    return md_path.parent / "audit.md"


def check_audit_evidence(
    md_path: pathlib.Path, state: str, *, layout: str = "directory"
) -> ConsistencyResult:
    """Check that a card at ``AUDITED``/``APPROVED`` has real audit evidence.

    The optional ``- **AUDITED:**`` provenance bullet in a card's
    ``## Status`` block is *not* evidence (``workflow.md`` makes it an
    optional addition to the history, not a required field) — the real
    signal is an audit file with a verdict of ``ready`` or
    ``ready_with_fixes``. Cards below ``AUDITED`` have nothing to check
    here.
    """
    if state not in ("AUDITED", "APPROVED"):
        return ConsistencyResult(True, f"audit evidence not required at {state}")
    audit_path = audit_path_for(md_path, layout=layout)
    if not audit_path.exists():
        return ConsistencyResult(
            False, f"{state} card has no audit evidence at {audit_path}"
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


def _mask_lifecycle_surface(md_text: str) -> str:
    """Strip/mask everything in ``md_text`` that is part of the lifecycle-
    tracking surface, leaving normative content untouched.

    Masked:

    - Every entire history bullet whose label is a recognised lifecycle
      state (``DRAFTED``/``EDITED``/``AUDITED``/``APPROVED``/``VALIDATED``/
      ``DEPRECATED``/``RETIRED``), including its wrapped continuation
      lines. These are append-only log entries: their count, order, and
      content are expected to grow with every transition, so the whole
      bullet is dropped rather than value-masked — a bullet that didn't
      exist before but exists now (a promotion, or a provenance backfill)
      must compare equal to a version that never had it.
    - The ``- **STATE:**`` bullet's value (it legitimately changes every
      transition).
    - The embedded fenced-YAML ``state:`` line's value (tolerant of
      leading indentation, for root-wrapped families like constitutions).
    - For the charter only: the free-text ``**Status:**`` header's value.

    Not masked: ``SOURCE:``, ``CREATED:``, ``MODIFIED:``, and any other
    STATUS-block field — a change to those is real provenance/content
    drift, not lifecycle bookkeeping (confirmed by this project's own
    history: SOURCE-line corrections always paired with a new ``EDITED:``
    bullet and correctly triggered re-audit).
    """
    lines = md_text.splitlines(keepends=True)
    out: list[str] = []
    in_history_bullet = False
    for line in lines:
        if _HISTORY_BULLET_RE.match(line):
            in_history_bullet = True
            continue
        if in_history_bullet:
            if line.strip() == "":
                in_history_bullet = False
                out.append(line)
                continue
            if line.startswith("- "):
                # A different bullet (e.g. SOURCE:, STATE:) — not a
                # continuation of the history bullet above.
                in_history_bullet = False
                out.append(line)
                continue
            # Indented wrapped-prose continuation line of the bullet above.
            continue
        out.append(line)
    masked = "".join(out)
    masked = _STATE_LINE_RE.sub(
        lambda m: m.group("prefix") + "<STATE>" + m.group("suffix"), masked
    )
    masked = re.sub(r"(?m)^(\s*state:[^\S\n]*)\S+[^\S\n]*$", r"\1<STATE>", masked)
    masked = _CHARTER_STATUS_LINE_RE.sub("**Status:** <STATUS>", masked)
    return masked


def check_audit_currency(
    *, current_md_text: str, audit_reference_md_text: str | None, state: str
) -> ConsistencyResult:
    """Check that an ``AUDITED``/``APPROVED`` card's content hasn't drifted
    since the audit evidence it's relying on.

    Compares ``current_md_text`` against ``audit_reference_md_text`` (the
    card's Markdown as of the commit that last touched its ``audit.md``)
    after masking the lifecycle-tracking surface from both (see
    :func:`_mask_lifecycle_surface`). If the masked versions are identical,
    the only changes since the audit were lifecycle bookkeeping — a
    provenance backfill or an ordinary ``prosoc-card-approve`` promotion —
    not real content drift, so this passes.

    ``audit_reference_md_text`` is ``None`` when no reliable reference
    point exists — ``audit.md`` has uncommitted changes (mid-edit), no git
    history, or doesn't exist yet. In that case this check is skipped
    (treated as consistent, not failed): guessing at an unstable reference
    point would itself be a new false-positive source, not a genuine
    staleness signal. Cards below ``AUDITED`` have nothing to check here.
    """
    if state not in ("AUDITED", "APPROVED"):
        return ConsistencyResult(True, f"audit currency not required at {state}")
    if audit_reference_md_text is None:
        return ConsistencyResult(
            True, "audit currency not checkable (no reliable git reference point)"
        )
    if _mask_lifecycle_surface(current_md_text) == _mask_lifecycle_surface(
        audit_reference_md_text
    ):
        return ConsistencyResult(True, "no content change since last audit")
    return ConsistencyResult(
        False,
        f"{state} card has content changes since its last audit "
        "(outside the lifecycle-tracking surface) -- re-audit required",
    )


def check_charter_status_line(md_text: str, state: str) -> ConsistencyResult:
    """Check the charter's free-text ``**Status:**`` line against ``state``.

    Case-insensitive match against the state's human-friendly label (see
    :data:`_STATUS_LINE_LABELS`), anchored to the *start* of the value and
    requiring a non-letter boundary right after it (end of string, or a
    descriptive suffix like " (Normative)") — the field is free text, not
    a controlled vocabulary, so this isn't a vocabulary-exact comparison,
    but a bare substring-anywhere search would wrongly accept contradictory
    headers: "Unapproved (Normative)" and "Draft (not approved)" both
    contain "approved" as a substring. A card with no such line (any
    non-charter family) has nothing to check.
    """
    value = parse_charter_status_line(md_text)
    if value is None:
        return ConsistencyResult(True, "no free-text Status: line present")
    label = _STATUS_LINE_LABELS.get(state, state.lower())
    normalized = value.strip().lower()
    if re.match(rf"^{re.escape(label)}(?![a-z])", normalized) is None:
        return ConsistencyResult(
            False, f"free-text Status: {value!r} does not reflect STATE {state!r}"
        )
    return ConsistencyResult(
        True, f"free-text Status: {value!r} matches STATE {state!r}"
    )
