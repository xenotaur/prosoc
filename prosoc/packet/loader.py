"""Generic card loader over a small family registry (Decision 4b).

One `CardLoader` loads any of the five card families named in a manifest into a
uniform :class:`LoadedCard`, keeping the payload opaque. The assembler needs
load -> schema-validate -> state-check -> embed-verbatim, not field-level access,
so no per-family Pydantic models are restated here (that would duplicate four
rich schemas and create a permanent drift surface, as ``charter/runtime.py``
itself warns). Schema validation happens **only** here — the single runtime
validation gate (mirroring ``charter/loader.py``).
"""

from __future__ import annotations

import functools
import hashlib
import json
import pathlib
from dataclasses import dataclass

import yaml
from jsonschema import ValidationError
from jsonschema.validators import validator_for

from prosoc.charter import distill as charter_distill
from prosoc.constitutions import distill as constitutions_distill
from prosoc.contexts import distill as contexts_distill
from prosoc.scenarios import distill as scenarios_distill
from prosoc.tasks import distill as tasks_distill
from prosoc.utils.cards import status

from .errors import ManifestError, ResolveError

# Repo root: prosoc/packet/loader.py -> parents[2] == <repo>.
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class PacketFamily:
    """How the loader locates and validates one card family."""

    name: str
    root: pathlib.Path
    schema_path: pathlib.Path
    # Card-per-directory families store <root>/<id>/<card_filename>; the charter
    # is a single document at <root>/<card_filename> (``single=True``).
    card_filename: str
    single: bool = False
    # Root-wrapped families (constitutions) nest the payload/state under a top
    # key; None means top-level.
    yaml_root_key: str | None = None

    def yml_path(self, card_id: str) -> pathlib.Path:
        if self.single:
            return self.root / self.card_filename
        return self.root / card_id / self.card_filename


def _family(name, module, card_filename, *, single=False, yaml_root_key=None):
    root = pathlib.Path(module.__file__).parent
    return PacketFamily(
        name=name,
        root=root,
        schema_path=root / "schema.json",
        card_filename=card_filename,
        single=single,
        yaml_root_key=yaml_root_key,
    )


FAMILIES: dict[str, PacketFamily] = {
    "scenarios": _family("scenarios", scenarios_distill, "scenario.yml"),
    "tasks": _family("tasks", tasks_distill, "task.yml"),
    "contexts": _family("contexts", contexts_distill, "context.yml"),
    "constitutions": _family(
        "constitutions",
        constitutions_distill,
        "constitution.yml",
        yaml_root_key="constitution",
    ),
    "charter": _family("charter", charter_distill, "charter.yml", single=True),
}


@functools.lru_cache
def _get_validator(schema_path: pathlib.Path):
    """Cache the compiled JSON schema validator (performance optimization)."""
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return validator_for(schema)(schema)


@dataclass(frozen=True)
class LoadedCard:
    """A resolved, schema-valid card ready to embed in a packet.

    ``payload`` is the full parsed YAML mapping, kept opaque; the assembler
    normalizes family root keys and strips ``state`` at assembly time.
    """

    family: str
    id: str
    path: str  # repo-relative POSIX path to the distilled *.yml
    sha256: str  # hex digest of the *.yml bytes (the embedded content)
    state: str
    payload: dict


def load_card(family: str, card_id: str) -> LoadedCard:
    """Load, schema-validate, and hash a single card.

    Raises:
        ManifestError: the family is not registered.
        ResolveError: the card file is missing, unparseable, schema-invalid,
            or lacks a lifecycle ``state``.
    """
    fam = FAMILIES.get(family)
    if fam is None:
        raise ManifestError(
            f"unknown family {family!r}; known families: {sorted(FAMILIES)}"
        )

    yml_path = fam.yml_path(card_id)
    if not yml_path.exists():
        raise ResolveError(f"{family}/{card_id}: no card at {_rel(yml_path)}")

    raw = yml_path.read_bytes()
    sha256 = hashlib.sha256(raw).hexdigest()

    try:
        payload = yaml.safe_load(raw.decode("utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ResolveError(
            f"{family}/{card_id}: could not parse card YAML: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise ResolveError(
            f"{family}/{card_id}: expected a top-level mapping in {_rel(yml_path)}"
        )

    # Single runtime validation gate.
    try:
        _get_validator(fam.schema_path).validate(instance=payload)
    except ValidationError as exc:
        raise ResolveError(
            f"{family}/{card_id}: schema validation failed: {exc.message}"
        ) from exc

    try:
        state = status.read_yaml_state(yml_path, root_key=fam.yaml_root_key)
    except status.StatusStateError as exc:
        raise ResolveError(f"{family}/{card_id}: {exc}") from exc

    return LoadedCard(
        family=family,
        id=card_id,
        path=_rel(yml_path),
        sha256=sha256,
        state=state,
        payload=payload,
    )


def _rel(path: pathlib.Path) -> str:
    """Repo-relative POSIX path for stable, portable provenance records."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()
