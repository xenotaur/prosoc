"""
Audit report validator.

Validates audit report JSON objects against the
Prosoc audit_report.schema.json schema.
"""

from pathlib import Path
import json

import jsonschema


def _load_validator():
    """
    Load and compile the audit report JSON schema from disk.
    """
    schema_path = Path(__file__).parent / "schema.json"

    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    # Validate the schema itself (raises if invalid)
    jsonschema.validators.Draft7Validator.check_schema(schema)

    # Compile the validator
    return jsonschema.validators.validator_for(schema)(schema)


# Load and compile schema once at import time
_AUDIT_REPORT_VALIDATOR = _load_validator()


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
    _AUDIT_REPORT_VALIDATOR.validate(instance=report)
