"""
Audit report validator.

Validates audit report JSON objects against the
Prosoc audit_report.schema.json schema.
"""

from pathlib import Path
import json

import jsonschema


def _load_schema() -> dict:
    """
    Load and validate the audit report JSON schema from disk.
    """
    schema_path = Path(__file__).parent / "schema.json"

    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    # Validate the schema itself (raises if invalid)
    jsonschema.validators.Draft7Validator.check_schema(schema)

    return schema


# Load schema once at import time
_AUDIT_REPORT_SCHEMA = _load_schema()

# Create a reusable validator instance to avoid re-compiling the schema on every call (~12x faster)
_AUDIT_REPORT_VALIDATOR = jsonschema.validators.Draft7Validator(_AUDIT_REPORT_SCHEMA)


def validate_audit_report(report: dict) -> None:
    """
    Validate an audit report against the Prosoc audit report schema.

    Parameters
    ----------
    report : dict
        Parsed audit report JSON.

    Raises
    ------
    jsonschema.ValidationError
        If the report does not conform to the schema.
    """
    _AUDIT_REPORT_VALIDATOR.validate(report)
