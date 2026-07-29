"""Fail-closed lifecycle gate (Decision 1/2, Saltzer & Schroeder fail-safe).

Default behaviour requires every member to have reached ``APPROVED`` (human
approval); if any member is below that floor the assembler emits nothing.
``--allow-unapproved`` lowers the floor to any live pre-approval state **and**
records the bypass in the payload (see :mod:`prosoc.packet.assemble`), so a
development packet is never byte-indistinguishable from a production one.
End-of-life states (``DEPRECATED``/``RETIRED``) never pass, hatch or not.
"""

from __future__ import annotations

from dataclasses import dataclass

# Monotonic production order; a card passes when its rank is at or above the
# active threshold's rank. States outside this list never pass.
PRODUCTION_ORDER: tuple[str, ...] = (
    "DRAFTED",
    "EDITED",
    "AUDITED",
    "APPROVED",
    "VALIDATED",
)
DISALLOWED: frozenset[str] = frozenset({"DEPRECATED", "RETIRED"})

PRODUCTION_THRESHOLD = "APPROVED"
DEVELOPMENT_THRESHOLD = "DRAFTED"


@dataclass(frozen=True)
class BlockedMember:
    family: str
    id: str
    state: str
    reason: str


@dataclass(frozen=True)
class GateResult:
    passed: bool
    threshold: str
    allow_unapproved: bool
    blocked: tuple[BlockedMember, ...]


def _rank(state: str) -> int | None:
    try:
        return PRODUCTION_ORDER.index(state)
    except ValueError:
        return None


def gate(cards, allow_unapproved: bool = False) -> GateResult:
    """Evaluate the lifecycle gate over resolved cards (fail-closed).

    ``cards`` is any iterable of objects exposing ``family``, ``id``, ``state``.
    """
    threshold = DEVELOPMENT_THRESHOLD if allow_unapproved else PRODUCTION_THRESHOLD
    floor = PRODUCTION_ORDER.index(threshold)

    blocked: list[BlockedMember] = []
    for card in cards:
        if card.state in DISALLOWED:
            blocked.append(
                BlockedMember(
                    card.family,
                    card.id,
                    card.state,
                    f"state {card.state} is end-of-life and never ships",
                )
            )
            continue
        rank = _rank(card.state)
        if rank is None:
            blocked.append(
                BlockedMember(
                    card.family,
                    card.id,
                    card.state,
                    f"state {card.state} is not a gateable lifecycle state",
                )
            )
            continue
        if rank < floor:
            blocked.append(
                BlockedMember(
                    card.family,
                    card.id,
                    card.state,
                    f"state {card.state} is below the {threshold} threshold",
                )
            )

    return GateResult(
        passed=not blocked,
        threshold=threshold,
        allow_unapproved=allow_unapproved,
        blocked=tuple(blocked),
    )
