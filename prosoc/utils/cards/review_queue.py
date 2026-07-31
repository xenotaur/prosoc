"""Corpus review-queue engine: rank cards by what most needs review.

Deterministic scan across all six registered card families producing a
ranked worklist for the human review/approval pass (see
``PROP-NORMATIVE-CARD-APPROVAL`` Decision 3). Reuses the ``FAMILIES``
registry (``prosoc.utils.cards.validate_status``) for discovery,
``prosoc.utils.cards.status`` for state reads, and
``prosoc.packet.gate.PRODUCTION_ORDER`` for the scope signal -- no new
discovery or state-reading logic.

Severity comes from each card's ``audit.md`` frontmatter (``blocking`` /
``should_fix`` / ``suggestion`` counts, produced by ``prosoc-card-audit``);
a card with no ``audit.md`` at all sorts as highest-severity, since it
cannot even be assessed for promotion yet. Run via
``scripts/validate/review-queue`` (a thin wrapper around
``python -m prosoc.utils.cards.review_queue``).
"""

from __future__ import annotations

import argparse
import json
import pathlib
from dataclasses import asdict, dataclass

import yaml

from prosoc.packet.gate import PRODUCTION_ORDER
from prosoc.utils.cards import status
from prosoc.utils.cards.validate_status import FAMILIES, Family

# Severity contribution per audit.md finding tier -- ordered so that a
# single blocking finding always outranks any number of should-fix/
# suggestion findings, and a single should-fix always outranks any number
# of suggestions.
_BLOCKING_WEIGHT = 100
_SHOULD_FIX_WEIGHT = 10
_SUGGESTION_WEIGHT = 1

# A card with no audit.md at all outranks every possible weighted sum of a
# card that has one (no realistic corpus produces a sum anywhere near this).
_NO_AUDIT_SEVERITY = 1_000_000

_SORTABLE_FIELDS = ("severity", "scope", "family", "id", "state")


@dataclass(frozen=True)
class QueueEntry:
    """One card's computed position in the review queue."""

    family: str
    id: str
    state: str
    scope: int
    has_audit: bool
    verdict: str | None
    blocking: int
    should_fix: int
    suggestion: int
    severity: int


def _label(source, family: Family) -> str:
    """Card id for display: the Markdown file stem for single-source
    families (``label_by_stem``), else its parent directory name. Mirrors
    ``validate_status._label``'s directory-layout branch -- the review
    queue only ever scans the real (directory-layout) corpus."""
    if family.label_by_stem:
        return source.md_path.stem
    return source.md_path.parent.name


def _scope(state: str) -> int:
    """Lifecycle steps remaining to APPROVED, floored at 0.

    States outside ``PRODUCTION_ORDER`` (``DEPRECATED``/``RETIRED``, or any
    unrecognised value) are end-of-life or invalid -- no promotion is
    meaningful, so they float to the bottom of the default ranking.
    """
    if state not in PRODUCTION_ORDER:
        return 0
    approved_rank = PRODUCTION_ORDER.index("APPROVED")
    state_rank = PRODUCTION_ORDER.index(state)
    return max(approved_rank - state_rank, 0)


def _read_audit(
    audit_path: pathlib.Path,
) -> tuple[bool, str | None, int, int, int]:
    """Parse an ``audit.md``'s YAML frontmatter.

    Returns ``(has_audit, verdict, blocking, should_fix, suggestion)``.
    A missing file, a file with no frontmatter block, or frontmatter that
    fails to parse as a YAML mapping are all treated identically as "no
    audit" -- a malformed audit.md must not silently rank as low severity.
    """
    if not audit_path.is_file():
        return False, None, 0, 0, 0
    text = audit_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False, None, 0, 0, 0
    parts = text.split("---", 2)
    if len(parts) < 3:
        return False, None, 0, 0, 0
    try:
        front = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return False, None, 0, 0, 0
    if not isinstance(front, dict):
        return False, None, 0, 0, 0
    verdict = front.get("verdict")
    try:
        blocking = int(front.get("blocking") or 0)
        should_fix = int(front.get("should_fix") or 0)
        suggestion = int(front.get("suggestion") or 0)
    except (TypeError, ValueError):
        # A non-numeric scalar (e.g. blocking: "many") is malformed
        # frontmatter, same as unparseable YAML -- fail closed to "no
        # audit" rather than crashing queue generation.
        return False, None, 0, 0, 0
    return True, verdict, blocking, should_fix, suggestion


def _severity(has_audit: bool, blocking: int, should_fix: int, suggestion: int) -> int:
    if not has_audit:
        return _NO_AUDIT_SEVERITY
    return (
        blocking * _BLOCKING_WEIGHT
        + should_fix * _SHOULD_FIX_WEIGHT
        + suggestion * _SUGGESTION_WEIGHT
    )


def build_queue(families: dict[str, Family] | None = None) -> list[QueueEntry]:
    """Scan every card in every given family and compute its queue entry.

    ``families`` defaults to the real registry; tests inject a
    ``dataclasses.replace(FAMILIES[name], default_root=tmp_root)`` mapping
    instead, mirroring ``validate_status_test.py``'s fixture pattern.
    """
    families = families if families is not None else FAMILIES
    entries: list[QueueEntry] = []
    for family in families.values():
        for source in family.discover(family.default_root, "directory"):
            state = status.read_yaml_state(
                source.yml_path, root_key=family.yaml_root_key
            )
            card_id = _label(source, family)
            audit_path = source.md_path.parent / "audit.md"
            has_audit, verdict, blocking, should_fix, suggestion = _read_audit(
                audit_path
            )
            entries.append(
                QueueEntry(
                    family=family.name,
                    id=card_id,
                    state=state,
                    scope=_scope(state),
                    has_audit=has_audit,
                    verdict=verdict,
                    blocking=blocking,
                    should_fix=should_fix,
                    suggestion=suggestion,
                    severity=_severity(has_audit, blocking, should_fix, suggestion),
                )
            )
    return entries


def sort_queue(
    entries: list[QueueEntry], sort: list[str], order: list[str]
) -> list[QueueEntry]:
    """Stable multi-key sort with independent per-field direction.

    ``sort``/``order`` are parallel lists. ``order`` may be shorter than
    ``sort`` (missing directions default to ``asc``), but must not be
    longer -- callers must validate that precondition themselves (``main``
    does, at the CLI boundary); a too-long ``order`` list is a caller bug,
    not a value this function will guess how to handle. A trailing
    ``(family, id)`` ascending tiebreak is always appended for determinism.
    Composed as a sequence of single-key stable sorts, most-significant
    key last -- Python's ``list.sort`` stability guarantees this correctly
    implements independent per-key directions.
    """
    keys = list(sort) + ["family", "id"]
    orders = list(order) + ["asc"] * (len(keys) - len(order))
    result = list(entries)
    for key, direction in reversed(list(zip(keys, orders, strict=True))):
        result.sort(key=lambda e, k=key: getattr(e, k), reverse=(direction == "desc"))
    return result


def format_table(entries: list[QueueEntry]) -> str:
    header = (
        f"{'FAMILY':<14} {'ID':<28} {'STATE':<10} {'SCOPE':>5} {'SEV':>7} "
        f"{'AUDIT':<6} VERDICT"
    )
    lines = [header, "-" * len(header)]
    for e in entries:
        audit = "yes" if e.has_audit else "NO"
        lines.append(
            f"{e.family:<14} {e.id:<28} {e.state:<10} {e.scope:>5} {e.severity:>7} "
            f"{audit:<6} {e.verdict or '-'}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rank prosoc normative cards by what most needs review."
    )
    parser.add_argument(
        "--family",
        choices=sorted(FAMILIES),
        default=None,
        help="Restrict to one card family (default: all registered families).",
    )
    parser.add_argument(
        "--sort",
        default="severity,scope",
        help=(
            "Comma-separated sort fields, most-significant first "
            f"(choices: {', '.join(_SORTABLE_FIELDS)})."
        ),
    )
    parser.add_argument(
        "--order",
        default="desc,desc",
        help="Comma-separated sort directions (asc|desc), matching --sort.",
    )
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Show only the top N entries after sorting.",
    )
    args = parser.parse_args(argv)

    sort_fields = [f.strip() for f in args.sort.split(",") if f.strip()]
    for f in sort_fields:
        if f not in _SORTABLE_FIELDS:
            parser.error(
                f"--sort: unknown field {f!r} "
                f"(choices: {', '.join(_SORTABLE_FIELDS)})"
            )
    order_dirs = [o.strip() for o in args.order.split(",") if o.strip()]
    for o in order_dirs:
        if o not in ("asc", "desc"):
            parser.error(f"--order: invalid direction {o!r} (choices: asc, desc)")
    if len(order_dirs) > len(sort_fields):
        parser.error(
            f"--order has {len(order_dirs)} direction(s) but --sort has only "
            f"{len(sort_fields)} field(s) -- --order must not be longer than --sort"
        )
    if args.limit is not None and args.limit < 0:
        parser.error("--limit must be >= 0")

    families = {args.family: FAMILIES[args.family]} if args.family else FAMILIES
    entries = build_queue(families)
    entries = sort_queue(entries, sort_fields, order_dirs)
    if args.limit is not None:
        entries = entries[: args.limit]

    if args.format == "json":
        print(json.dumps([asdict(e) for e in entries], indent=2))
    else:
        print(format_table(entries))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
