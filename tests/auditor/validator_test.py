import json
import unittest
from pathlib import Path

import jsonschema

from prosoc.auditor import validator


class TestAuditReportValidator(unittest.TestCase):
    """
    Unit tests for the Prosoc audit report JSON schema validator.
    """

    def setUp(self):
        """
        Load the golden audit report fixture from the prosoc package data.
        """
        project_root = Path(__file__).resolve().parents[2]
        golden_path = (
            project_root / "tests" / "auditor" / "data" / "golden_audit_report.json"
        )

        with golden_path.open("r", encoding="utf-8") as f:
            self.golden_report = json.load(f)
        self.assertIsNotNone(self.golden_report)

    def test_golden_audit_report_is_valid(self):
        """
        A known-good (golden) audit report should validate
        without raising an exception.
        """
        try:
            validator.validate_audit_report(self.golden_report)
        except Exception as e:
            self.fail(f"Golden audit report should be valid, but raised: {e}")

    def test_missing_required_summary_field_fails_validation(self):
        """
        Removing a required field should cause schema validation to fail.
        """
        bad_report = json.loads(json.dumps(self.golden_report))  # deep copy

        # Remove a required field
        del bad_report["summary"]["error_count"]

        with self.assertRaises(jsonschema.ValidationError):
            validator.validate_audit_report(bad_report)


if __name__ == "__main__":
    unittest.main()
