"""
loader.py

Loader and validation boundary for the Prosocial Robot Navigation Charter.

This module is responsible for:
- Loading the generated `charter.yml`
- Validating it against the canonical JSON Schema (`schema.json`)
- Instantiating runtime Pydantic models for downstream use

IMPORTANT:
- This is the *only* place where schema validation should occur at runtime.
- `runtime.py` assumes all data has already passed this gate.
"""

import json
import pathlib
from typing import Optional

import yaml
from jsonschema import validate as jsonschema_validate, ValidationError as SchemaValidationError

from prosoc.charter import runtime


# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

CHARTER_DIR = pathlib.Path(__file__).parent
DEFAULT_CHARTER_YAML = CHARTER_DIR / "charter.yml"
DEFAULT_SCHEMA_JSON = CHARTER_DIR / "schema.json"


# -----------------------------------------------------------------------------
# Loader API
# -----------------------------------------------------------------------------

def load_charter(
    charter_path: pathlib.Path = DEFAULT_CHARTER_YAML,
    schema_path: pathlib.Path = DEFAULT_SCHEMA_JSON,
) -> runtime.Charter:
    """
    Load, validate, and instantiate the Prosocial Robot Navigation Charter.

    Args:
        charter_path: Path to the generated charter.yml file.
        schema_path: Path to the canonical JSON Schema.

    Returns:
        A `runtime.Charter` instance containing validated principles.

    Raises:
        FileNotFoundError: If the charter or schema file does not exist.
        yaml.YAMLError: If the YAML cannot be parsed.
        SchemaValidationError: If the charter violates the schema.
        pydantic.ValidationError: If runtime instantiation fails.
    """
    if not charter_path.exists():
        raise FileNotFoundError(f"Charter file not found: {charter_path}")

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    # Load YAML charter
    with charter_path.open("r", encoding="utf-8") as f:
        raw_charter = yaml.safe_load(f)

    # Load JSON Schema
    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    # Validate against schema (normative gate)
    jsonschema_validate(instance=raw_charter, schema=schema)

    # Instantiate runtime representation (ergonomic layer)
    return runtime.Charter(**raw_charter)


# -----------------------------------------------------------------------------
# Convenience helpers
# -----------------------------------------------------------------------------

def load_principles(
    charter_path: pathlib.Path = DEFAULT_CHARTER_YAML,
    schema_path: pathlib.Path = DEFAULT_SCHEMA_JSON,
) -> list[runtime.CharterPrinciple]:
    """
    Convenience wrapper returning only the list of principles.

    This mirrors the legacy API but preserves the new architecture.
    """
    charter = load_charter(charter_path=charter_path, schema_path=schema_path)
    return charter.principles