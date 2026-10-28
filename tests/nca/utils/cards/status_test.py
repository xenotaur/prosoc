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


AUDIT_MD = """\
---
family: scenarios
card: example
verdict: {verdict}
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-01-01
---

# Audit: Example
"""


class ReadAuditVerdictTest(unittest.TestCase):
    def test_reads_verdict(self):
        with tempfile.TemporaryDirectory() as d:
            audit = Path(d) / "audit.md"
            audit.write_text(AUDIT_MD.format(verdict="ready"), encoding="utf-8")
            self.assertEqual(status.read_audit_verdict(audit), "ready")

    def test_missing_verdict_key_returns_none(self):
        with tempfile.TemporaryDirectory() as d:
            audit = Path(d) / "audit.md"
            audit.write_text("---\nfamily: scenarios\n---\n", encoding="utf-8")
            self.assertIsNone(status.read_audit_verdict(audit))

    def test_no_frontmatter_returns_none(self):
        with tempfile.TemporaryDirectory() as d:
            audit = Path(d) / "audit.md"
            audit.write_text(
                "# Audit: Example\n\nNo frontmatter here.\n", encoding="utf-8"
            )
            self.assertIsNone(status.read_audit_verdict(audit))

    def test_malformed_yaml_returns_none_does_not_raise(self):
        # Malformed YAML (unclosed bracket) must not raise yaml.YAMLError --
        # one bad audit.md must fail only its own card's check, not abort
        # an entire corpus scan.
        with tempfile.TemporaryDirectory() as d:
            audit = Path(d) / "audit.md"
            audit.write_text("---\nverdict: [ready\n---\n", encoding="utf-8")
            self.assertIsNone(status.read_audit_verdict(audit))


class CheckAuditEvidenceTest(unittest.TestCase):
    def test_below_audited_requires_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "card.md"
            md.write_text("placeholder", encoding="utf-8")
            for state in ("DRAFTED", "EDITED"):
                self.assertTrue(status.check_audit_evidence(md, state).ok)

    def test_approved_with_ready_audit_passes(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "card.md"
            md.write_text("placeholder", encoding="utf-8")
            (Path(d) / "audit.md").write_text(
                AUDIT_MD.format(verdict="ready"), encoding="utf-8"
            )
            self.assertTrue(status.check_audit_evidence(md, "APPROVED").ok)

    def test_audited_with_ready_with_fixes_passes(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "card.md"
            md.write_text("placeholder", encoding="utf-8")
            (Path(d) / "audit.md").write_text(
                AUDIT_MD.format(verdict="ready_with_fixes"), encoding="utf-8"
            )
            self.assertTrue(status.check_audit_evidence(md, "AUDITED").ok)

    def test_approved_missing_audit_md_fails(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "card.md"
            md.write_text("placeholder", encoding="utf-8")
            result = status.check_audit_evidence(md, "APPROVED")
            self.assertFalse(result.ok)
            self.assertIn("no audit evidence", result.detail)

    def test_flat_layout_uses_card_specific_audit_file(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "card_b.md"
            md.write_text("placeholder", encoding="utf-8")
            (Path(d) / "card_b.audit.md").write_text(
                AUDIT_MD.format(verdict="ready"), encoding="utf-8"
            )
            result = status.check_audit_evidence(md, "APPROVED", layout="flat")
            self.assertTrue(result.ok)

    def test_flat_layout_does_not_accept_another_cards_shared_audit_md(self):
        # Regression: a bare sibling `audit.md` in a flat root must not
        # "prove" audit evidence for every card sharing that root -- only
        # this card's own <stem>.audit.md counts in flat layout.
        with tempfile.TemporaryDirectory() as d:
            md_a = Path(d) / "card_a.md"
            md_a.write_text("placeholder", encoding="utf-8")
            md_b = Path(d) / "card_b.md"
            md_b.write_text("placeholder", encoding="utf-8")
            (Path(d) / "card_a.audit.md").write_text(
                AUDIT_MD.format(verdict="ready"), encoding="utf-8"
            )
            result_a = status.check_audit_evidence(md_a, "APPROVED", layout="flat")
            result_b = status.check_audit_evidence(md_b, "APPROVED", layout="flat")
            self.assertTrue(result_a.ok)
            self.assertFalse(result_b.ok)
            self.assertIn("no audit evidence", result_b.detail)

    def test_directory_layout_is_the_default(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "card.md"
            md.write_text("placeholder", encoding="utf-8")
            (Path(d) / "audit.md").write_text(
                AUDIT_MD.format(verdict="ready"), encoding="utf-8"
            )
            # No explicit layout= passed: directory-layout sibling lookup.
            self.assertTrue(status.check_audit_evidence(md, "APPROVED").ok)

    def test_approved_with_malformed_audit_yaml_fails_without_raising(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "card.md"
            md.write_text("placeholder", encoding="utf-8")
            (Path(d) / "audit.md").write_text(
                "---\nverdict: [ready\n---\n", encoding="utf-8"
            )
            result = status.check_audit_evidence(md, "APPROVED")
            self.assertFalse(result.ok)

    def test_approved_with_blocking_verdict_fails(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "card.md"
            md.write_text("placeholder", encoding="utf-8")
            (Path(d) / "audit.md").write_text(
                AUDIT_MD.format(verdict="blocking"), encoding="utf-8"
            )
            result = status.check_audit_evidence(md, "APPROVED")
            self.assertFalse(result.ok)
            self.assertIn("no acceptable verdict", result.detail)


CHARTER_HEADER = (
    "# Charter\n\n**Version:** 0.1  \n**Status:** {status}  \n**Scope:** x  \n"
)


class CheckCharterStatusLineTest(unittest.TestCase):
    def test_parses_status_line(self):
        text = CHARTER_HEADER.format(status="Approved (Normative)")
        self.assertEqual(status.parse_charter_status_line(text), "Approved (Normative)")

    def test_no_status_line_returns_none(self):
        self.assertIsNone(status.parse_charter_status_line("# Charter\n\nNo field.\n"))

    def test_matching_status_passes(self):
        text = CHARTER_HEADER.format(status="Approved (Normative)")
        self.assertTrue(status.check_charter_status_line(text, "APPROVED").ok)

    def test_stale_status_fails(self):
        text = CHARTER_HEADER.format(status="Draft (Normative)")
        result = status.check_charter_status_line(text, "APPROVED")
        self.assertFalse(result.ok)
        self.assertIn("does not reflect STATE", result.detail)

    def test_absent_status_line_passes_trivially(self):
        # A non-charter card has no such line; nothing to check.
        self.assertTrue(
            status.check_charter_status_line(
                "# Scenario: X\n\nNo field.\n", "APPROVED"
            ).ok
        )

    def test_unapproved_does_not_satisfy_approved(self):
        # A bare substring search would wrongly accept this: "approved" is
        # a substring of "unapproved". The actual lifecycle label must be
        # anchored at the start of the value, not found anywhere in it.
        text = CHARTER_HEADER.format(status="Unapproved (Normative)")
        result = status.check_charter_status_line(text, "APPROVED")
        self.assertFalse(result.ok)

    def test_draft_not_approved_does_not_satisfy_approved(self):
        text = CHARTER_HEADER.format(status="Draft (not approved)")
        result = status.check_charter_status_line(text, "APPROVED")
        self.assertFalse(result.ok)

    def test_unaudited_does_not_satisfy_audited(self):
        text = CHARTER_HEADER.format(status="Unaudited (Normative)")
        result = status.check_charter_status_line(text, "AUDITED")
        self.assertFalse(result.ok)


class ScenariosShimTest(unittest.TestCase):
    """The scenarios re-export shim exposes the same objects as the shared module."""

    def test_shim_reexports_shared_symbols(self):
        from prosoc.prnc.scenarios import status as shim

        self.assertIs(shim.check_source, status.check_source)
        self.assertIs(shim.StatusStateError, status.StatusStateError)
        self.assertEqual(shim.STATES, status.STATES)


if __name__ == "__main__":
    unittest.main()
