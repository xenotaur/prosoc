import unittest
from typing import Any, Dict

import jsonschema

from prosoc.auditor.orchestrator import audit_normative_card
from prosoc.auditor.validator import validate_audit_report


class FakeLLM:
    """
    Deterministic fake LLM for testing the auditor orchestration logic.

    It returns a pre-specified JSON object regardless of prompt content.
    """

    def __init__(self, response: Dict[str, Any]):
        self._response = response

    def complete(
        self, *, system_prompt: str, user_prompt: str, model_name: str | None = None
    ) -> Dict[str, Any]:
        # In the real LLM client, this would call the OpenAI API.
        # For testing, we simply return the canned response.
        return self._response


class TestAuditNormativeCard(unittest.TestCase):
    """Unit tests for audit_normative_card using a FakeLLM."""

    def setUp(self):
        # Minimal but schema-valid audit report
        self.valid_audit_report = {
            "audit_metadata": {
                "auditor": "prosoc-auditor",
                "model": "default",
                "timestamp": "2026-01-18T00:00:00Z",
                "audit_version": "0.1",
            },
            "card_metadata": {
                "card_id": "test_card",
                "card_type": "scenario",
                "source_path": "tests/data/scenario.md",
            },
            "schema_validation": {
                "valid": True,
                "errors": [],
            },
            "internal_consistency": {
                "status": "pass",
                "issues": [],
            },
            "reference_consistency": {
                "status": "not_evaluated",
                "issues": [],
            },
            "summary": {
                "error_count": 0,
                "warning_count": 0,
                "note_count": 0,
                "recommendations": [],
                "confidence": "high",
            },
        }

        # Invalid report: missing required field in summary
        self.invalid_audit_report = {
            "audit_metadata": self.valid_audit_report["audit_metadata"],
            "internal_consistency": self.valid_audit_report["internal_consistency"],
            "reference_consistency": self.valid_audit_report["reference_consistency"],
            "summary": {
                "error_count": 0,
                "warning_count": 0,
                # info_count missing
            },
        }

        # Dummy card inputs
        self.card_kwargs = dict(
            card_id="test_card",
            card_type="scenario",
            source_path="tests/data/scenario.md",
            markdown_text="# Test Scenario\nSome prose.",
            yaml_dict={"id": "test_card"},
            reference_excerpts=None,
        )

    def test_audit_normative_card_with_valid_llm_output(self):
        """
        audit_normative_card should return a validated audit report
        when the LLM output conforms to the schema.
        """
        fake_llm = FakeLLM(self.valid_audit_report)

        report = audit_normative_card(
            llm_client=fake_llm,
            **self.card_kwargs,
        )

        # Should not raise
        validate_audit_report(report)

        self.assertEqual(report["internal_consistency"]["status"], "pass")
        self.assertEqual(report["summary"]["error_count"], 0)

    def test_audit_normative_card_with_invalid_llm_output_raises(self):
        """
        audit_normative_card should raise when the LLM output
        does not conform to the audit schema.
        """
        fake_llm = FakeLLM(self.invalid_audit_report)

        with self.assertRaises(jsonschema.ValidationError):
            audit_normative_card(
                llm_client=fake_llm,
                **self.card_kwargs,
            )


if __name__ == "__main__":
    unittest.main()
