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


class MaskLifecycleSurfaceTest(unittest.TestCase):
    def test_strips_history_bullets_and_continuations(self):
        text = (
            "- **STATE:** APPROVED\n"
            "- **SOURCE:** x\n"
            "- **EDITED:** Claude, 2026-11-06 -- demoted\n"
            "  from APPROVED to EDITED\n"
            "- **AUDITED:** Claude, 2026-08-01\n"
            "- **VALIDATED:** --\n"
        )
        masked = status._mask_lifecycle_surface(text)
        self.assertEqual(masked, "- **STATE:** <STATE>\n- **SOURCE:** x\n")

    def test_masks_state_bullet_value_only(self):
        masked = status._mask_lifecycle_surface(
            "- **STATE:** EDITED\n- **SOURCE:** x\n"
        )
        self.assertIn("- **STATE:** <STATE>\n", masked)
        self.assertIn("- **SOURCE:** x\n", masked)

    def test_masks_fenced_yaml_state_line(self):
        masked = status._mask_lifecycle_surface(
            "summary: y\nstate: APPROVED\nname: z\n"
        )
        self.assertIn("state: <STATE>\n", masked)
        self.assertNotIn("APPROVED", masked)

    def test_masks_indented_root_wrapped_yaml_state_line(self):
        # Constitutions nest state under a `constitution:` key -- only
        # masked when the caller says so via yaml_root_key.
        masked = status._mask_lifecycle_surface(
            "constitution:\n  state: APPROVED\n", yaml_root_key="constitution"
        )
        self.assertIn("  state: <STATE>\n", masked)

    def test_unindented_state_not_masked_when_yaml_root_key_given(self):
        # A root-wrapped family's real state: is at 2-space indent, not 0 --
        # the top-level (unindented) form must not be masked for it.
        masked = status._mask_lifecycle_surface(
            "state: APPROVED\n", yaml_root_key="constitution"
        )
        self.assertEqual(masked, "state: APPROVED\n")

    def test_indented_state_not_masked_for_flat_families(self):
        # The inverse: a flat family's real state: is at column 0 -- a line
        # that merely happens to be indented and read "state: X" (e.g.
        # prose inside a different field's YAML block scalar) must not be
        # masked, since it is not the authoritative lifecycle field.
        text = "evaluation_notes: |\n  state: blocked\n  more text\nstate: APPROVED\n"
        masked = status._mask_lifecycle_surface(text)
        self.assertIn("state: blocked", masked)
        self.assertIn("state: <STATE>\n", masked)

    def test_state_value_change_inside_a_block_scalar_is_not_hidden(self):
        # Regression: a block scalar's own prose happening to read
        # "state: <word>" must never be masked -- found and fixed via
        # PR-mode review (PR #137). If it were masked, real content drift
        # confined to that prose would be invisible to the comparison.
        before = "evaluation_notes: |\n  state: blocked\nstate: APPROVED\n"
        after = "evaluation_notes: |\n  state: clear\nstate: APPROVED\n"
        self.assertNotEqual(
            status._mask_lifecycle_surface(before),
            status._mask_lifecycle_surface(after),
        )

    def test_masks_state_value_with_trailing_inline_comment(self):
        # Regression: a lifecycle state with an inline YAML comment (valid
        # YAML syntax) must still be masked, with the comment text
        # preserved for comparison -- found and fixed via PR-mode review
        # (PR #137).
        masked = status._mask_lifecycle_surface("state: AUDITED # reviewed\n")
        self.assertEqual(masked, "state: <STATE> # reviewed\n")

    def test_promotion_with_inline_comment_still_compares_equal(self):
        before = "state: AUDITED # reviewed\n"
        after = "state: APPROVED # reviewed\n"
        self.assertEqual(
            status._mask_lifecycle_surface(before),
            status._mask_lifecycle_surface(after),
        )

    def test_masks_charter_status_header_value(self):
        masked = status._mask_lifecycle_surface("**Status:** Approved (Normative)  \n")
        self.assertIn("**Status:** <STATUS>", masked)

    def test_does_not_mask_source_or_other_fields(self):
        # SOURCE/CREATED/MODIFIED are content/provenance, not lifecycle
        # bookkeeping -- a change here must still show up after masking.
        masked = status._mask_lifecycle_surface(
            "- **SOURCE:** original\n- **CREATED:** 2026-01-01\n"
        )
        self.assertIn("- **SOURCE:** original\n", masked)
        self.assertIn("- **CREATED:** 2026-01-01\n", masked)

    def test_a_different_bullet_right_after_a_history_bullet_is_not_swallowed(self):
        # A non-lifecycle bullet (e.g. SOURCE:) right after a history bullet
        # must be recognised as its own bullet, not treated as a
        # continuation line of the one before -- only VALIDATED/DRAFTED/etc.
        # (themselves in STATES) are expected to be stripped too.
        text = "- **AUDITED:** Claude, 2026-08-01\n- **SOURCE:** x\n"
        masked = status._mask_lifecycle_surface(text)
        self.assertIn("- **SOURCE:** x\n", masked)

    def test_indented_continuation_line_is_stripped_even_if_it_starts_with_hyphen(self):
        # A genuine wrapped continuation line is recognised by indentation
        # alone, regardless of what text it starts with.
        text = (
            "- **EDITED:** Claude, 2026-11-06 -- demoted\n"
            "  - from APPROVED to EDITED (indented, starts with a hyphen)\n"
            "- **SOURCE:** x\n"
        )
        masked = status._mask_lifecycle_surface(text)
        self.assertEqual(masked, "- **SOURCE:** x\n")

    def test_unindented_non_bullet_line_right_after_a_history_bullet_is_preserved(self):
        # An unindented line that is *not* itself a recognised bullet (e.g.
        # a malformed/unconventional continuation, or just stray text) is
        # never silently dropped -- only indentation marks a continuation.
        # This is the safe direction: if such a line's content ever changes,
        # it shows up as a real diff (should-fix via re-audit) rather than
        # vanishing from the comparison.
        text = (
            "- **EDITED:** Claude, 2026-11-06 -- demoted\n"
            "- from APPROVED to EDITED (unindented, not a recognised bullet)\n"
            "- **SOURCE:** x\n"
        )
        masked = status._mask_lifecycle_surface(text)
        self.assertEqual(
            masked,
            "- from APPROVED to EDITED (unindented, not a recognised bullet)\n"
            "- **SOURCE:** x\n",
        )

    def test_heading_immediately_after_the_last_bullet_is_not_swallowed(self):
        # Regression: a Markdown heading (or any other real content) with
        # no blank line before it, directly after the last history bullet,
        # must never be mistaken for a continuation line and dropped -- a
        # genuine prior bug, found and fixed via PR-mode review (PR #137).
        text = (
            "- **AUDITED:** Claude, 2026-08-01\n"
            "## Normative Expectations\n\nThe robot must do X.\n"
        )
        masked = status._mask_lifecycle_surface(text)
        self.assertEqual(masked, "## Normative Expectations\n\nThe robot must do X.\n")

    def test_back_to_back_history_bullets_with_no_blank_line_both_stripped(self):
        text = (
            "- **AUDITED:** Claude, 2026-08-01\n"
            "- **APPROVED:** Claude, 2026-11-07\n"
            "- **SOURCE:** x\n"
        )
        masked = status._mask_lifecycle_surface(text)
        self.assertEqual(masked, "- **SOURCE:** x\n")


class CheckAuditCurrencyTest(unittest.TestCase):
    def test_below_audited_requires_nothing(self):
        for state in ("DRAFTED", "EDITED"):
            result = status.check_audit_currency(
                current_md_text="anything",
                audit_reference_md_text="anything else",
                state=state,
            )
            self.assertTrue(result.ok)

    def test_no_reference_point_skips_the_check(self):
        # No reliable git reference (uncommitted audit.md, no history, etc.)
        # must never itself be treated as evidence of staleness.
        result = status.check_audit_currency(
            current_md_text="- **STATE:** APPROVED\n\nchanged content\n",
            audit_reference_md_text=None,
            state="APPROVED",
        )
        self.assertTrue(result.ok)
        self.assertIn("not checkable", result.detail)

    def test_genuine_content_drift_fails(self):
        before = "- **STATE:** APPROVED\n\nThe robot must do X.\n"
        after = "- **STATE:** APPROVED\n\nThe robot must do Y.\n"
        result = status.check_audit_currency(
            current_md_text=after, audit_reference_md_text=before, state="APPROVED"
        )
        self.assertFalse(result.ok)
        self.assertIn("content changes since its last audit", result.detail)

    def test_provenance_backfill_only_does_not_false_positive(self):
        # The real WI-CHARTER-SUPPLEMENT-AUDIT-EVIDENCE-BACKFILL case (PR
        # #128): a blank AUDITED bullet filled in with a date copied from
        # the card's own audit.md -- no content change.
        before = (
            "- **STATE:** APPROVED\n- **SOURCE:** x\n- **AUDITED:** --\n"
            "- **VALIDATED:** --\n\nThe robot must do X.\n"
        )
        after = (
            "- **STATE:** APPROVED\n- **SOURCE:** x\n"
            "- **AUDITED:** Claude (prosoc-card-audit skill), 2026-08-01\n"
            "- **VALIDATED:** --\n\nThe robot must do X.\n"
        )
        result = status.check_audit_currency(
            current_md_text=after, audit_reference_md_text=before, state="APPROVED"
        )
        self.assertTrue(result.ok)

    def test_ordinary_promotion_commit_does_not_false_positive(self):
        # The real WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION case: a
        # prosoc-card-approve run changes STATE, the fenced-YAML state:
        # line, and adds one new history bullet -- no content change.
        before = (
            "- **STATE:** AUDITED\n- **SOURCE:** x\n"
            "- **AUDITED:** Claude, 2026-08-01\n- **VALIDATED:** --\n\n"
            "The robot must do X.\n\nstate: AUDITED\n"
        )
        after = (
            "- **STATE:** APPROVED\n- **SOURCE:** x\n"
            "- **AUDITED:** Claude, 2026-08-01\n"
            "- **APPROVED:** Claude (WI), 2026-11-07 (PR #136)\n"
            "- **VALIDATED:** --\n\n"
            "The robot must do X.\n\nstate: APPROVED\n"
        )
        result = status.check_audit_currency(
            current_md_text=after, audit_reference_md_text=before, state="APPROVED"
        )
        self.assertTrue(result.ok)

    def test_new_history_bullet_with_hidden_content_change_still_fails(self):
        # A promotion-shaped diff is not a blank check -- a real content
        # change riding along with a new bullet must still be caught.
        before = "- **STATE:** AUDITED\n\nThe robot must do X.\n"
        after = (
            "- **STATE:** APPROVED\n"
            "- **APPROVED:** Claude (WI), 2026-11-07\n\n"
            "The robot must do Y.\n"
        )
        result = status.check_audit_currency(
            current_md_text=after, audit_reference_md_text=before, state="APPROVED"
        )
        self.assertFalse(result.ok)

    def test_yaml_only_content_drift_fails(self):
        # Regression: the work item's own acceptance criteria name
        # "Markdown or distilled YAML" explicitly -- a direct edit to the
        # distilled *.yml that never touches the Markdown at all (bypassing
        # the normal authoring workflow) must still be caught. Found and
        # fixed via PR-mode review (PR #137).
        md = "- **STATE:** APPROVED\n\nThe robot must do X.\n"
        result = status.check_audit_currency(
            current_md_text=md,
            audit_reference_md_text=md,
            state="APPROVED",
            current_yml_text="id: x\nstate: APPROVED\nsummary: new\n",
            audit_reference_yml_text="id: x\nstate: AUDITED\nsummary: old\n",
        )
        self.assertFalse(result.ok)
        self.assertIn("distilled YAML", result.detail)

    def test_yaml_state_only_change_does_not_false_positive(self):
        # The YAML-side equivalent of an ordinary promotion: only the
        # state field differs.
        md = "- **STATE:** APPROVED\n\nThe robot must do X.\n"
        result = status.check_audit_currency(
            current_md_text=md,
            audit_reference_md_text=md,
            state="APPROVED",
            current_yml_text="id: x\nstate: APPROVED\nsummary: same\n",
            audit_reference_yml_text="id: x\nstate: AUDITED\nsummary: same\n",
        )
        self.assertTrue(result.ok)

    def test_yaml_comparison_skipped_when_not_provided(self):
        # Callers that don't pass YAML text at all (or it fails to parse)
        # get Markdown-only comparison, same as before this field existed
        # -- never a reason to fail on its own.
        md = "- **STATE:** APPROVED\n\nThe robot must do X.\n"
        result = status.check_audit_currency(
            current_md_text=md, audit_reference_md_text=md, state="APPROVED"
        )
        self.assertTrue(result.ok)

    def test_root_wrapped_yaml_state_only_change_does_not_false_positive(self):
        md = "- **STATE:** APPROVED\n\nThe robot must do X.\n"
        result = status.check_audit_currency(
            current_md_text=md,
            audit_reference_md_text=md,
            state="APPROVED",
            yaml_root_key="constitution",
            current_yml_text="constitution:\n  id: x\n  state: APPROVED\n  rules: []\n",
            audit_reference_yml_text=(
                "constitution:\n  id: x\n  state: AUDITED\n  rules: []\n"
            ),
        )
        self.assertTrue(result.ok)


class MaskYamlStateTest(unittest.TestCase):
    def test_removes_top_level_state(self):
        masked = status._mask_yaml_state("id: x\nstate: APPROVED\n")
        self.assertEqual(masked, {"id": "x"})

    def test_removes_root_wrapped_state(self):
        masked = status._mask_yaml_state(
            "constitution:\n  id: x\n  state: APPROVED\n", yaml_root_key="constitution"
        )
        self.assertEqual(masked, {"constitution": {"id": "x"}})

    def test_malformed_yaml_returns_none(self):
        self.assertIsNone(status._mask_yaml_state("id: [unterminated\n"))

    def test_non_mapping_yaml_returns_none(self):
        self.assertIsNone(status._mask_yaml_state("- just\n- a\n- list\n"))


class AuditPathForTest(unittest.TestCase):
    def test_directory_layout_uses_sibling_audit_md(self):
        p = status.audit_path_for(Path("/root/card/card.md"), layout="directory")
        self.assertEqual(p, Path("/root/card/audit.md"))

    def test_flat_layout_uses_stem_specific_audit_md(self):
        p = status.audit_path_for(Path("/root/card_b.md"), layout="flat")
        self.assertEqual(p, Path("/root/card_b.audit.md"))


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
