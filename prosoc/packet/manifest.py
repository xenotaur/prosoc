"""Minimal manifest input for the assembler (Decision 3, Option 4).

Phase 1 reads a plain YAML manifest that names member cards by ``family`` + card
locator ``id``. Making the manifest a full auditable card family (its own
``manifest.md`` + template + distiller + schema) is Phase 2; this module defines
only what ``resolve`` needs.

Example::

    builder: "prosoc packet assembler"
    members:
      - {family: charter, id: charter}
      - {family: scenarios, id: intersection_gesture_wait}
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass

import yaml

from .errors import ManifestError


@dataclass(frozen=True)
class Member:
    family: str
    id: str


@dataclass(frozen=True)
class Manifest:
    members: tuple[Member, ...]
    builder: str | None = None


def load_manifest(path: pathlib.Path) -> Manifest:
    """Parse a manifest file into a :class:`Manifest`.

    Raises:
        ManifestError: the file is missing, unparseable, or malformed.
    """
    if not path.exists():
        raise ManifestError(f"manifest not found: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ManifestError(f"invalid manifest YAML: {exc}") from exc
    return parse_manifest(data)


def parse_manifest(data: object) -> Manifest:
    if not isinstance(data, dict):
        raise ManifestError("manifest must be a mapping")

    raw_members = data.get("members")
    if not isinstance(raw_members, list) or not raw_members:
        raise ManifestError("manifest must have a non-empty 'members' list")

    members: list[Member] = []
    for i, entry in enumerate(raw_members):
        if not isinstance(entry, dict):
            raise ManifestError(f"member[{i}] must be a mapping")
        family = entry.get("family")
        card_id = entry.get("id")
        if not isinstance(family, str) or not family:
            raise ManifestError(f"member[{i}] is missing a string 'family'")
        if not isinstance(card_id, str) or not card_id:
            raise ManifestError(f"member[{i}] is missing a string 'id'")
        members.append(Member(family=family, id=card_id))

    seen: set[tuple[str, str]] = set()
    for m in members:
        key = (m.family, m.id)
        if key in seen:
            raise ManifestError(f"duplicate member: {m.family}/{m.id}")
        seen.add(key)

    builder = data.get("builder")
    if builder is not None and not isinstance(builder, str):
        raise ManifestError("'builder' must be a string when present")

    return Manifest(members=tuple(members), builder=builder)
