"""Compose resolved cards into a namespaced provenance envelope (Decision 5/6).

The envelope is **namespaced, never a deep merge** — ``scenario.yml`` already
has a top-level ``context:`` key that would silently collide with a context
card, and merging erases provenance. It is shaped as an in-toto statement
(``_type`` / ``subject`` / ``predicate_type`` / ``predicate``) with a reserved,
DSSE-shaped ``signatures: []`` slot, split into two audiences:

* ``guidance`` — what the agent consumes (``state`` stripped, family root keys
  normalized, principles unioned per Decision 6). ``subject.digest`` covers the
  serialized ``guidance`` block only, so a detached copy stays verifiable.
* ``predicate`` — what the auditor consumes (builder identity; each card's id,
  family, path, content hash, and lifecycle state).
"""

from __future__ import annotations

import copy
import functools
import hashlib
import json
import pathlib

from jsonschema import ValidationError
from jsonschema.validators import validator_for

from . import gate as gate_mod
from .errors import AssembleError
from .loader import LoadedCard
from .manifest import Manifest

SCHEMA_PATH = pathlib.Path(__file__).parent / "schema.json"

STATEMENT_TYPE = "https://in-toto.io/Statement/v1"
PREDICATE_TYPE = "https://prosocial-robotics.org/NormativePacket/v1"

NON_PRODUCTION_NOTICE = (
    "This guidance was not human-approved: the lifecycle gate was bypassed via "
    "--allow-unapproved. Do not use in production."
)

_EMPHASIS_RANK = {"emphasized": 2, "deprioritized": 1, "neutral": 0}


def _strip_state(payload: dict) -> dict:
    out = copy.deepcopy(payload)
    out.pop("state", None)
    return out


def _guidance_body(card: LoadedCard) -> dict:
    """Card payload as it appears under ``guidance``: root-key normalized and
    ``state`` stripped."""
    if card.family == "constitutions":
        inner = card.payload.get("constitution")
        if not isinstance(inner, dict):
            raise AssembleError(
                f"constitutions/{card.id}: payload is not root-wrapped under "
                "'constitution'"
            )
        return _strip_state(inner)
    return _strip_state(card.payload)


def _principle_union(by_family: dict[str, dict[str, LoadedCard]]) -> list[dict]:
    """Decision 6: union of scenario.relevant_principles,
    task.related_principles, and context.principle_emphasis.emphasized, each
    annotated with an emphasis; deprioritized principles are annotated, never
    dropped. Charter detail is joined when the charter is a member.
    """
    emphasis: dict[str, str] = {}

    def note(pid: str, level: str) -> None:
        if _EMPHASIS_RANK[level] > _EMPHASIS_RANK.get(emphasis.get(pid, "neutral"), 0):
            emphasis[pid] = level
        else:
            emphasis.setdefault(pid, level)

    for card in by_family.get("scenarios", {}).values():
        for pid in card.payload.get("relevant_principles", []) or []:
            note(pid, "neutral")
    for card in by_family.get("tasks", {}).values():
        for pid in card.payload.get("related_principles", []) or []:
            note(pid, "neutral")
    for card in by_family.get("contexts", {}).values():
        pe = card.payload.get("principle_emphasis") or {}
        for pid in pe.get("emphasized", []) or []:
            note(pid, "emphasized")
        for pid in pe.get("deprioritized", []) or []:
            note(pid, "deprioritized")

    # Charter detail, if the charter is a member.
    detail: dict[str, dict] = {}
    order: dict[str, int] = {}
    charter = by_family.get("charter", {}).get("charter")
    if charter is not None:
        for i, principle in enumerate(charter.payload.get("principles", []) or []):
            pid = principle.get("id")
            if pid is not None:
                detail[pid] = principle
                order[pid] = i

    principles: list[dict] = []
    for pid in sorted(emphasis, key=lambda p: (order.get(p, 10_000), p)):
        entry = copy.deepcopy(detail.get(pid, {"id": pid}))
        entry["emphasis"] = emphasis[pid]
        principles.append(entry)
    return principles


def _tensions(by_family: dict[str, dict[str, LoadedCard]]) -> dict:
    """Surface both interpretive-tension mechanisms; reconcile neither."""
    common: list[dict] = []
    for card in by_family.get("contexts", {}).values():
        pe = card.payload.get("principle_emphasis") or {}
        items = pe.get("common_tensions") or []
        if items:
            common.append({"context": card.id, "tensions": list(items)})

    conflicts: list[dict] = []
    for card in by_family.get("constitutions", {}).values():
        inner = card.payload.get("constitution") or {}
        cr = inner.get("conflict_resolution")
        if cr is not None:
            conflicts.append({"constitution": card.id, "conflict_resolution": cr})

    return {"common_tensions": common, "conflict_resolution": conflicts}


def _below_production(state: str) -> bool:
    """True if a state is below the production (APPROVED) floor, or is an
    end-of-life / ungateable state (defensive: the gate blocks these upstream)."""
    if state in gate_mod.DISALLOWED or state not in gate_mod.PRODUCTION_ORDER:
        return True
    floor = gate_mod.PRODUCTION_ORDER.index(gate_mod.PRODUCTION_THRESHOLD)
    return gate_mod.PRODUCTION_ORDER.index(state) < floor


def _canonical_digest(block: dict) -> str:
    serialized = json.dumps(
        block, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def assemble(
    cards: list[LoadedCard],
    manifest: Manifest,
    *,
    allow_unapproved: bool = False,
    justification: str | None = None,
) -> dict:
    """Build the provenance envelope from resolved, gate-passing cards.

    The escape hatch is stamped into the payload (``predicate.policy`` and a
    ``guidance.notice``) whenever the packet actually contains a card below the
    production (``APPROVED``) floor — never merely because the flag was passed.
    """
    if not cards:
        raise AssembleError("cannot assemble an empty packet")

    by_family: dict[str, dict[str, LoadedCard]] = {}
    for card in cards:
        by_family.setdefault(card.family, {})[card.id] = card

    # guidance — namespaced by family then id (uniform across families,
    # including the single-source charter); no deep merge.
    guidance: dict = {}
    for card in cards:
        guidance.setdefault(card.family, {})[card.id] = _guidance_body(card)

    guidance["principles"] = _principle_union(by_family)
    guidance["tensions"] = _tensions(by_family)

    sub_approved = [c for c in cards if _below_production(c.state)]
    hatch_engaged = allow_unapproved and bool(sub_approved)
    if hatch_engaged:
        if not justification:
            raise AssembleError(
                "engaging --allow-unapproved requires a written justification"
            )
        guidance["notice"] = NON_PRODUCTION_NOTICE

    escape_hatch = None
    if hatch_engaged:
        escape_hatch = {
            "justification": justification,
            "bypassed_threshold": gate_mod.PRODUCTION_THRESHOLD,
            "cards_below_threshold": [
                {"family": c.family, "id": c.id, "state": c.state} for c in sub_approved
            ],
        }

    predicate = {
        "builder": {"id": manifest.builder or "unspecified"},
        "policy": {
            "gate_threshold": (
                gate_mod.DEVELOPMENT_THRESHOLD
                if allow_unapproved
                else gate_mod.PRODUCTION_THRESHOLD
            ),
            "allow_unapproved": allow_unapproved,
            "escape_hatch": escape_hatch,
        },
        "resolved_cards": [
            {
                "family": c.family,
                "id": c.id,
                "path": c.path,
                "sha256": c.sha256,
                "state": c.state,
            }
            for c in cards
        ],
    }

    envelope = {
        "_type": STATEMENT_TYPE,
        "subject": [
            {"name": "guidance", "digest": {"sha256": _canonical_digest(guidance)}}
        ],
        "predicate_type": PREDICATE_TYPE,
        "predicate": predicate,
        "guidance": guidance,
        "signatures": [],
    }
    validate_envelope(envelope)
    return envelope


@functools.lru_cache
def _get_validator():
    """Cache the compiled JSON schema validator (performance optimization)."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return validator_for(schema)(schema)


def validate_envelope(envelope: dict) -> None:
    """Validate an assembled envelope against ``packet.schema.json``.

    Raises:
        AssembleError: the envelope does not conform to the schema.
    """
    try:
        _get_validator().validate(instance=envelope)
    except ValidationError as exc:
        raise AssembleError(
            f"assembled packet failed schema validation: {exc.message}"
        ) from exc
