# Unit tests for prosoc.utils.cards.review_queue

import dataclasses
import tempfile
import unittest
from pathlib import Path

from prosoc.utils.cards import review_queue
from prosoc.utils.cards.validate_status import FAMILIES

MD = """\
# Card: Example

## Status

- **STATE:** DRAFTED
- **SOURCE:** somewhere

---
"""

AUDIT = """\
---
family: scenarios
card: {card}
verdict: {verdict}
blocking: {blocking}
should_fix: {should_fix}
suggestion: {suggestion}
audited: 2026-07-31
---

# Audit: Example
"""


def _dir_card(root: Path, name: str, yml_state: str, stem: str = "scenario") -> Path:
    """Directory-layout card: <root>/<name>/<stem>.md and <stem>.yml. Returns
    the card's directory (where audit.md, if any, would also live)."""
    d = root / name
    d.mkdir()
    (d / f"{stem}.md").write_text(MD, encoding="utf-8")
    (d / f"{stem}.yml").write_text(
        f"id: {name}_01\nname: {name}\nstate: {yml_state}\nsummary: y\n",
        encoding="utf-8",
    )
    return d


def _family_at(name: str, root: Path):
    """A registry entry for ``name`` pointed at a temp root, reusing the
    real family's discover callable -- mirrors validate_status_test.py's
    fixture pattern via a root override rather than a fresh Family."""
    return dataclasses.replace(FAMILIES[name], default_root=root)


class ScopeTest(unittest.TestCase):
    def test_drafted_is_three_steps_from_approved(self):
        self.assertEqual(review_queue._scope("DRAFTED"), 3)

    def test_edited_is_two_steps(self):
        self.assertEqual(review_queue._scope("EDITED"), 2)

    def test_audited_is_one_step(self):
        self.assertEqual(review_queue._scope("AUDITED"), 1)

    def test_approved_is_zero_steps(self):
        self.assertEqual(review_queue._scope("APPROVED"), 0)

    def test_validated_floors_at_zero(self):
        # VALIDATED is past APPROVED in PRODUCTION_ORDER; no further
        # promotion is meaningful, so scope floors at 0 rather than going
        # negative.
        self.assertEqual(review_queue._scope("VALIDATED"), 0)

    def test_end_of_life_state_is_zero(self):
        self.assertEqual(review_queue._scope("DEPRECATED"), 0)
        self.assertEqual(review_queue._scope("RETIRED"), 0)

    def test_unrecognised_state_is_zero(self):
        self.assertEqual(review_queue._scope("BOGUS"), 0)


class ReadAuditTest(unittest.TestCase):
    def test_missing_file_reports_no_audit(self):
        with tempfile.TemporaryDirectory() as d:
            result = review_queue._read_audit(Path(d) / "audit.md")
            self.assertEqual(result, (False, None, 0, 0, 0))

    def test_valid_frontmatter_parsed(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "audit.md"
            path.write_text(
                AUDIT.format(
                    card="x",
                    verdict="ready_with_fixes",
                    blocking=1,
                    should_fix=2,
                    suggestion=3,
                ),
                encoding="utf-8",
            )
            has_audit, verdict, blocking, should_fix, suggestion = (
                review_queue._read_audit(path)
            )
            self.assertTrue(has_audit)
            self.assertEqual(verdict, "ready_with_fixes")
            self.assertEqual((blocking, should_fix, suggestion), (1, 2, 3))

    def test_no_frontmatter_block_reports_no_audit(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "audit.md"
            path.write_text(
                "# Audit: Example\n\nNo frontmatter here.\n", encoding="utf-8"
            )
            self.assertEqual(review_queue._read_audit(path), (False, None, 0, 0, 0))

    def test_malformed_yaml_reports_no_audit(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "audit.md"
            path.write_text("---\nfamily: [unclosed\n---\n", encoding="utf-8")
            self.assertEqual(review_queue._read_audit(path), (False, None, 0, 0, 0))

    def test_non_mapping_frontmatter_reports_no_audit(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "audit.md"
            path.write_text("---\n- just\n- a\n- list\n---\n", encoding="utf-8")
            self.assertEqual(review_queue._read_audit(path), (False, None, 0, 0, 0))


class SeverityTest(unittest.TestCase):
    def test_no_audit_outranks_any_weighted_sum(self):
        # Even a pathologically high-finding audited card must rank below
        # a card with no audit.md at all.
        worst_audited = review_queue._severity(
            True, blocking=1000, should_fix=1000, suggestion=1000
        )
        self.assertLess(worst_audited, review_queue._NO_AUDIT_SEVERITY)

    def test_blocking_outranks_any_should_fix_or_suggestion_count(self):
        one_blocking = review_queue._severity(
            True, blocking=1, should_fix=0, suggestion=0
        )
        many_should_fix = review_queue._severity(
            True, blocking=0, should_fix=9, suggestion=9
        )
        self.assertGreater(one_blocking, many_should_fix)

    def test_should_fix_outranks_any_suggestion_count(self):
        one_should_fix = review_queue._severity(
            True, blocking=0, should_fix=1, suggestion=0
        )
        many_suggestions = review_queue._severity(
            True, blocking=0, should_fix=0, suggestion=9
        )
        self.assertGreater(one_should_fix, many_suggestions)

    def test_clean_audit_is_zero(self):
        self.assertEqual(review_queue._severity(True, 0, 0, 0), 0)


class BuildQueueTest(unittest.TestCase):
    def test_scans_cards_and_reads_audit(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            audited_dir = _dir_card(root, "audited", "DRAFTED")
            (audited_dir / "audit.md").write_text(
                AUDIT.format(
                    card="audited",
                    verdict="ready",
                    blocking=0,
                    should_fix=0,
                    suggestion=0,
                ),
                encoding="utf-8",
            )
            _dir_card(root, "unaudited", "DRAFTED")

            entries = review_queue.build_queue(
                {"scenarios": _family_at("scenarios", root)}
            )
            by_id = {e.id: e for e in entries}

            self.assertEqual(len(entries), 2)
            self.assertTrue(by_id["audited"].has_audit)
            self.assertEqual(by_id["audited"].verdict, "ready")
            self.assertEqual(by_id["audited"].severity, 0)
            self.assertFalse(by_id["unaudited"].has_audit)
            self.assertEqual(
                by_id["unaudited"].severity, review_queue._NO_AUDIT_SEVERITY
            )

    def test_scope_reflects_card_state(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "edited", "EDITED")
            entries = review_queue.build_queue(
                {"scenarios": _family_at("scenarios", root)}
            )
            self.assertEqual(entries[0].scope, 2)

    def test_empty_root_yields_no_entries(self):
        with tempfile.TemporaryDirectory() as d:
            entries = review_queue.build_queue(
                {"scenarios": _family_at("scenarios", Path(d))}
            )
            self.assertEqual(entries, [])


class SortQueueTest(unittest.TestCase):
    def _entry(self, family, id_, severity, scope):
        return review_queue.QueueEntry(
            family=family,
            id=id_,
            state="DRAFTED",
            scope=scope,
            has_audit=True,
            verdict="ready",
            blocking=0,
            should_fix=0,
            suggestion=0,
            severity=severity,
        )

    def test_default_severity_desc_then_scope_desc(self):
        low = self._entry("scenarios", "low", severity=1, scope=1)
        high = self._entry("scenarios", "high", severity=9, scope=1)
        mid = self._entry("scenarios", "mid", severity=5, scope=3)
        result = review_queue.sort_queue(
            [low, high, mid], ["severity", "scope"], ["desc", "desc"]
        )
        self.assertEqual([e.id for e in result], ["high", "mid", "low"])

    def test_independent_per_field_direction(self):
        a = self._entry("scenarios", "a", severity=1, scope=9)
        b = self._entry("scenarios", "b", severity=2, scope=1)
        # severity desc (b before a), scope asc as a tiebreak that never
        # applies here since severities differ -- exercises that mixed
        # asc/desc directions are accepted without error.
        result = review_queue.sort_queue([a, b], ["severity", "scope"], ["desc", "asc"])
        self.assertEqual([e.id for e in result], ["b", "a"])

    def test_ties_break_by_family_then_id(self):
        z = self._entry("tasks", "z", severity=5, scope=1)
        a = self._entry("scenarios", "a", severity=5, scope=1)
        result = review_queue.sort_queue([z, a], ["severity"], ["desc"])
        self.assertEqual(
            [(e.family, e.id) for e in result], [("scenarios", "a"), ("tasks", "z")]
        )

    def test_no_audit_card_sorts_first_under_default_ranking(self):
        clean = self._entry("scenarios", "clean", severity=0, scope=3)
        no_audit = review_queue.QueueEntry(
            family="scenarios",
            id="gap",
            state="DRAFTED",
            scope=3,
            has_audit=False,
            verdict=None,
            blocking=0,
            should_fix=0,
            suggestion=0,
            severity=review_queue._NO_AUDIT_SEVERITY,
        )
        result = review_queue.sort_queue(
            [clean, no_audit], ["severity", "scope"], ["desc", "desc"]
        )
        self.assertEqual(result[0].id, "gap")


class CliIntegrationTest(unittest.TestCase):
    def test_default_run_over_real_repo_covers_whole_corpus(self):
        # Integration smoke test against the live corpus: every card family
        # must be discoverable and every card must produce a queue entry,
        # regardless of individual audit/state values.
        entries = review_queue.build_queue()
        self.assertEqual(len(entries), 32)
        families_seen = {e.family for e in entries}
        self.assertEqual(
            families_seen,
            {"scenarios", "tasks", "contexts", "constitutions", "charter", "manifests"},
        )

    def test_main_json_output_is_valid_and_sorted(self):
        import io
        import json
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            code = review_queue.main(["--format", "json"])
        self.assertEqual(code, 0)
        entries = json.loads(buf.getvalue())
        self.assertEqual(len(entries), 32)
        severities = [e["severity"] for e in entries]
        self.assertEqual(severities, sorted(severities, reverse=True))

    def test_main_rejects_unknown_sort_field(self):
        with self.assertRaises(SystemExit):
            review_queue.main(["--sort", "bogus"])

    def test_main_rejects_invalid_order(self):
        with self.assertRaises(SystemExit):
            review_queue.main(["--order", "sideways"])

    def test_main_family_filter_scopes_output(self):
        import io
        import json
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            review_queue.main(["--family", "charter", "--format", "json"])
        entries = json.loads(buf.getvalue())
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["family"], "charter")

    def test_main_limit_truncates(self):
        import io
        import json
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            review_queue.main(["--format", "json", "--limit", "3"])
        entries = json.loads(buf.getvalue())
        self.assertEqual(len(entries), 3)


if __name__ == "__main__":
    unittest.main()
