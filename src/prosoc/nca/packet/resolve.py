"""Resolve a manifest into ordered, loaded cards."""

from __future__ import annotations

from .loader import LoadedCard, load_card
from .manifest import Manifest


def resolve(manifest: Manifest) -> list[LoadedCard]:
    """Load every manifest member, preserving manifest order.

    Raises:
        ManifestError: a member names an unknown family.
        ResolveError: a member does not resolve to a loadable, valid card.
    """
    return [load_card(m.family, m.id) for m in manifest.members]
