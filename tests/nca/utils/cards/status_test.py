# Unit tests for prosoc.nca.utils.cards.status (shared, family-agnostic helpers)

import tempfile
import unittest
from pathlib import Path

from prosoc.nca.utils.cards import status


STATUS_BLOCK = """\
# Card: Example

## Status

- **STATE:** DRAFTED
- **SOURCE:** somewhere
- **DRAFTED:** someone, 2026-01-01

---
"""

# Uppercase heading with a STATE line that ends in two trailing spaces — the
# Markdown line-break style real task cards use. Built with explicit escapes so
# the trailing spaces live inside the string, not on the source line.
STATUS_BLOCK_UPPER = (
    "# Task: Example\n\n"
    "## STATUS\n"
    "- **STATE:** DRAFTED  \n"
    "- **SOURCE:** somewhere\n\n"
    "---\n"
)


class ParseMarkdownStateTest(unittest.TestCase):
    def test_parses_state(self):
        self.assertEqual(status.parse_markdown_state(STATUS_BLOCK), "DRAFTED")

    def test_parses_state_uppercase_heading_with_trailing_ws(self):
        self.assertEqual(status.parse_markdown_state(STATUS_BLOCK_UPPER), "DRAFTED")

    def test_missing_state_raises(self):
        with self.assertRaises(status.StatusStateError):
            status.parse_markdown_state("## Status\n\n- **SOURCE:** x\n")


class ProjectStateTest(unittest.TestCase):
    def test_projects_new_state(self):
        out = status.project_state_into_markdown(STATUS_BLOCK, "APPROVED")
        self.assertIn("- **STATE:** APPROVED", out)
        self.assertNotIn("- **STATE:** DRAFTED", out)
        self.assertIn("- **SOURCE:** somewhere", out)

    def test_projection_is_idempotent(self):
        once = status.project_state_into_markdown(STATUS_BLOCK, "EDITED")
        twice = status.project_state_into_markdown(once, "EDITED")
        self.assertEqual(once, twice)

    def test_projection_preserves_trailing_whitespace(self):
        # Task cards use two trailing spaces on the STATE bullet; projecting a
        # new state must swap only the token and keep the trailing whitespace.
        out = status.project_state_into_markdown(STATUS_BLOCK_UPPER, "APPROVED")
        self.assertIn("- **STATE:** APPROVED  \n", out)

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
            yml = Path(d) / "card.yml"
            yml.write_text(
                "id: x\nname: X\nstate: AUDITED\nsummary: y\n", encoding="utf-8"
            )
            self.assertEqual(status.read_yaml_state(yml), "AUDITED")

    def test_read_yaml_state_missing(self):
        with tempfile.TemporaryDirectory() as d:
            yml = Path(d) / "card.yml"
            yml.write_text("id: x\nname: X\nsummary: y\n", encoding="utf-8")
            with self.assertRaises(status.StatusStateError):
                status.read_yaml_state(yml)

    def test_read_yaml_state_root_key(self):
        # Root-wrapped payload (as constitutions use): state nests under the key.
        with tempfile.TemporaryDirectory() as d:
            yml = Path(d) / "constitution.yml"
            yml.write_text(
                "constitution:\n  id: x\n  name: X\n  state: EDITED\n",
                encoding="utf-8",
            )
            self.assertEqual(
                status.read_yaml_state(yml, root_key="constitution"), "EDITED"
            )

    def test_read_yaml_state_root_key_missing_mapping(self):
        with tempfile.TemporaryDirectory() as d:
            yml = Path(d) / "constitution.yml"
            yml.write_text("id: x\nname: X\nstate: EDITED\n", encoding="utf-8")
            with self.assertRaises(status.StatusStateError):
                status.read_yaml_state(yml, root_key="constitution")

    def test_check_source_root_key(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "constitution.md"
            yml = Path(d) / "constitution.yml"
            md.write_text(STATUS_BLOCK.replace("DRAFTED", "EDITED"), encoding="utf-8")
            yml.write_text(
                "constitution:\n  id: x\n  name: X\n  state: EDITED\n",
                encoding="utf-8",
            )
            self.assertTrue(status.check_source(md, yml, root_key="constitution").ok)

    def test_check_source_consistent(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "card.md"
            yml = Path(d) / "card.yml"
            md.write_text(STATUS_BLOCK, encoding="utf-8")
            yml.write_text(
                "id: x\nname: X\nstate: DRAFTED\nsummary: y\n", encoding="utf-8"
            )
            self.assertTrue(status.check_source(md, yml).ok)

    def test_check_source_inconsistent(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "card.md"
            yml = Path(d) / "card.yml"
            md.write_text(STATUS_BLOCK, encoding="utf-8")  # DRAFTED
            yml.write_text(
                "id: x\nname: X\nstate: APPROVED\nsummary: y\n", encoding="utf-8"
            )
            self.assertFalse(status.check_source(md, yml).ok)


class ScenariosShimTest(unittest.TestCase):
    """The scenarios re-export shim exposes the same objects as the shared module."""

    def test_shim_reexports_shared_symbols(self):
        from prosoc.prnc.scenarios import status as shim

        self.assertIs(shim.check_source, status.check_source)
        self.assertIs(shim.StatusStateError, status.StatusStateError)
        self.assertEqual(shim.STATES, status.STATES)


if __name__ == "__main__":
    unittest.main()
