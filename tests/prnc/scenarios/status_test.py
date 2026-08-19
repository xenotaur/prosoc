# Unit tests for prosoc.prnc.scenarios.status

import tempfile
import unittest
from pathlib import Path

from prosoc.prnc.scenarios import status


STATUS_BLOCK = """\
# Scenario: Example

## Status

- **STATE:** DRAFTED
- **SOURCE:** somewhere
- **DRAFTED:** someone, 2026-01-01

---
"""


class ParseMarkdownStateTest(unittest.TestCase):
    def test_parses_state(self):
        self.assertEqual(status.parse_markdown_state(STATUS_BLOCK), "DRAFTED")

    def test_missing_state_raises(self):
        with self.assertRaises(status.StatusStateError):
            status.parse_markdown_state("## Status\n\n- **SOURCE:** x\n")


class ProjectStateTest(unittest.TestCase):
    def test_projects_new_state(self):
        out = status.project_state_into_markdown(STATUS_BLOCK, "APPROVED")
        self.assertIn("- **STATE:** APPROVED", out)
        self.assertNotIn("- **STATE:** DRAFTED", out)
        # Provenance lines are untouched.
        self.assertIn("- **SOURCE:** somewhere", out)

    def test_projection_is_idempotent(self):
        once = status.project_state_into_markdown(STATUS_BLOCK, "EDITED")
        twice = status.project_state_into_markdown(once, "EDITED")
        self.assertEqual(once, twice)

    def test_unknown_state_raises(self):
        with self.assertRaises(ValueError):
            status.project_state_into_markdown(STATUS_BLOCK, "BOGUS")

    def test_no_state_line_raises(self):
        with self.assertRaises(status.StatusStateError):
            status.project_state_into_markdown(
                "## Status\n\n- **SOURCE:** x\n", "DRAFTED"
            )


class CheckConsistencyTest(unittest.TestCase):
    def test_agreement(self):
        result = status.check_consistency(
            markdown_state="DRAFTED", yaml_state="DRAFTED"
        )
        self.assertTrue(result.ok)

    def test_disagreement(self):
        result = status.check_consistency(
            markdown_state="DRAFTED", yaml_state="APPROVED"
        )
        self.assertFalse(result.ok)
        self.assertIn("!=", result.detail)

    def test_unknown_yaml_state(self):
        result = status.check_consistency(markdown_state="DRAFTED", yaml_state="NOPE")
        self.assertFalse(result.ok)
        self.assertIn("not a recognised state", result.detail)


class FileHelpersTest(unittest.TestCase):
    def test_read_yaml_state(self):
        with tempfile.TemporaryDirectory() as d:
            yml = Path(d) / "scenario.yml"
            yml.write_text(
                "id: x\nname: X\nstate: AUDITED\nsummary: y\n", encoding="utf-8"
            )
            self.assertEqual(status.read_yaml_state(yml), "AUDITED")

    def test_read_yaml_state_missing(self):
        with tempfile.TemporaryDirectory() as d:
            yml = Path(d) / "scenario.yml"
            yml.write_text("id: x\nname: X\nsummary: y\n", encoding="utf-8")
            with self.assertRaises(status.StatusStateError):
                status.read_yaml_state(yml)

    def test_check_source_consistent(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "scenario.md"
            yml = Path(d) / "scenario.yml"
            md.write_text(STATUS_BLOCK, encoding="utf-8")
            yml.write_text(
                "id: x\nname: X\nstate: DRAFTED\nsummary: y\n", encoding="utf-8"
            )
            self.assertTrue(status.check_source(md, yml).ok)

    def test_check_source_inconsistent(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "scenario.md"
            yml = Path(d) / "scenario.yml"
            md.write_text(STATUS_BLOCK, encoding="utf-8")  # DRAFTED
            yml.write_text(
                "id: x\nname: X\nstate: APPROVED\nsummary: y\n", encoding="utf-8"
            )
            self.assertFalse(status.check_source(md, yml).ok)


if __name__ == "__main__":
    unittest.main()
