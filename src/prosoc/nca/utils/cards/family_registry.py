"""Shared card-family identity.

The packet loader (``prosoc.nca.packet.loader``) and the lifecycle-status
validator (``prosoc.nca.utils.cards.validate_status``) each register the
same five card families, but need different things from them: the loader
needs a schema path and a card filename; the status validator needs a
discovery function and flat-layout support. This module is the one place
that names each family and resolves its root directory and the two
special cases (``constitutions``'s root-wrapped YAML, ``charter``'s
single-document layout), so the two consumers can't drift out of sync on
those shared facts.
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass

from prosoc.constitutions import distill as constitutions_distill
from prosoc.prnc.charter import distill as charter_distill
from prosoc.prnc.contexts import distill as contexts_distill
from prosoc.prnc.scenarios import distill as scenarios_distill
from prosoc.prnc.tasks import distill as tasks_distill


@dataclass(frozen=True)
class CardFamilyIdentity:
    """A card family's identity, shared by every consumer that registers it.

    ``single`` marks the one family (``charter``) that is a single document
    at ``<root>/<filename>`` rather than one card per
    ``<root>/<id>/<filename>`` directory. ``yaml_root_key`` marks a family
    whose distilled YAML nests the payload (and lifecycle ``state``) under
    a top-level key instead of storing it inline.
    """

    name: str
    root: pathlib.Path
    yaml_root_key: str | None = None
    single: bool = False


def _identity(name: str, module, **kwargs) -> CardFamilyIdentity:
    return CardFamilyIdentity(
        name=name, root=pathlib.Path(module.__file__).parent, **kwargs
    )


CARD_FAMILIES: dict[str, CardFamilyIdentity] = {
    "scenarios": _identity("scenarios", scenarios_distill),
    "tasks": _identity("tasks", tasks_distill),
    "contexts": _identity("contexts", contexts_distill),
    "constitutions": _identity(
        "constitutions", constitutions_distill, yaml_root_key="constitution"
    ),
    "charter": _identity("charter", charter_distill, single=True),
}
