# Integration tests for prosoc.packet.cli against the sample manifest.

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from prosoc.packet import cli
from prosoc.packet.assemble import PREDICATE_TYPE
from prosoc.packet.loader import REPO_ROOT

SAMPLE = REPO_ROOT / "prosoc" / "manifests" / "sample_packet" / "manifest.yml"
GOLDEN = REPO_ROOT / "prosoc" / "manifests" / "sample_packet" / "packet.golden.yml"


def _run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()


def _write_unapproved_manifest(tmp_dir: Path) -> Path:
    """A manifest naming one real card that is guaranteed to stay below the
    production floor: blind_corner is not part of the WI-CARD-APPROVAL-PILOT
    promotion, so it remains DRAFTED. sample_packet's own members are now
    all APPROVED (the pilot's whole point) and can no longer demonstrate the
    fail-closed gate or the --allow-unapproved escape hatch -- this fixture
    exercises those paths generically instead."""
    manifest_path = tmp_dir / "unapproved_manifest.yml"
    manifest_path.write_text(
        "builder: test\nmembers:\n- family: scenarios\n  id: blind_corner\n",
        encoding="utf-8",
    )
    return manifest_path


class CliTest(unittest.TestCase):
    def test_sample_manifest_exists(self):
        self.assertTrue(SAMPLE.exists())

    def test_fail_closed_blocks_a_manifest_with_an_unapproved_member(self):
        with tempfile.TemporaryDirectory() as d:
            manifest = _write_unapproved_manifest(Path(d))
            code, out, err = _run([str(manifest)])
            self.assertEqual(code, 1)
            self.assertEqual(out, "")
            self.assertIn("fail-closed", err)

    def test_sample_packet_default_now_succeeds_since_pilot_approved(self):
        # The corpus's first production-mode packet: all 5 sample_packet
        # members reached APPROVED in WI-CARD-APPROVAL-PILOT, so the
        # default (no --allow-unapproved) gate now passes for real.
        code, out, err = _run([str(SAMPLE)])
        self.assertEqual(code, 0)
        env = yaml.safe_load(out)
        self.assertEqual(env["predicate"]["policy"]["gate_threshold"], "APPROVED")
        self.assertFalse(env["predicate"]["policy"]["allow_unapproved"])
        self.assertIsNone(env["predicate"]["policy"]["escape_hatch"])
        self.assertNotIn("notice", env["guidance"])

    def test_allow_unapproved_emits_valid_packet_with_hatch_engaged(self):
        with tempfile.TemporaryDirectory() as d:
            manifest = _write_unapproved_manifest(Path(d))
            code, out, err = _run(
                [str(manifest), "--allow-unapproved", "integration test"]
            )
            self.assertEqual(code, 0)
            env = yaml.safe_load(out)
            self.assertEqual(env["predicate_type"], PREDICATE_TYPE)
            self.assertIn("notice", env["guidance"])
            self.assertTrue(env["predicate"]["policy"]["escape_hatch"])

    def test_allow_unapproved_on_fully_approved_manifest_does_not_engage_hatch(self):
        # --allow-unapproved only stamps the escape hatch when it is actually
        # needed (assemble.py: hatch_engaged = allow_unapproved and
        # bool(sub_approved)) -- passing it against an all-APPROVED manifest
        # is a no-op on the hatch fields, though allow_unapproved/
        # gate_threshold still record the flag itself.
        code, out, err = _run([str(SAMPLE), "--allow-unapproved", "integration test"])
        self.assertEqual(code, 0)
        env = yaml.safe_load(out)
        self.assertTrue(env["predicate"]["policy"]["allow_unapproved"])
        self.assertEqual(env["predicate"]["policy"]["gate_threshold"], "DRAFTED")
        self.assertIsNone(env["predicate"]["policy"]["escape_hatch"])
        self.assertNotIn("notice", env["guidance"])

    def test_empty_justification_rejected(self):
        code, _, err = _run([str(SAMPLE), "--allow-unapproved", "   "])
        self.assertEqual(code, 2)
        self.assertIn("justification", err)

    def test_missing_manifest(self):
        code, _, err = _run([str(REPO_ROOT / "nope.yml")])
        self.assertEqual(code, 1)
        self.assertIn("not found", err)

    def test_check_matches_the_checked_in_golden(self):
        # sample_packet's golden is production-mode (see
        # prosoc/packet/README.md) -- no --allow-unapproved here, or the
        # rendered packet's policy fields would no longer match the golden.
        code, out, err = _run([str(SAMPLE), "--check"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "")
        self.assertEqual(err, "")

    def test_check_rejects_format_json(self):
        code, out, err = _run([str(SAMPLE), "--check", "--format", "json"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("--format json", err)


class CliCheckTest(unittest.TestCase):
    """--check tests against a scratch manifest dir, so drift/missing cases
    never touch the checked-in golden. Member resolution is repo-root
    relative, so a manifest copied elsewhere still resolves real cards."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.manifest = self.tmp / "manifest.yml"
        shutil.copy(SAMPLE, self.manifest)
        self.golden = self.tmp / "packet.golden.yml"

    def _check(self):
        # No --allow-unapproved: matches how sample_packet's real golden is
        # now generated (production mode, all members APPROVED).
        return _run([str(self.manifest), "--check"])

    def test_matching_golden_exits_zero_silently(self):
        shutil.copy(GOLDEN, self.golden)
        code, out, err = self._check()
        self.assertEqual(code, 0)
        self.assertEqual(out, "")
        self.assertEqual(err, "")

    def test_drifted_golden_exits_one_with_diff(self):
        self.golden.write_text("this is not a packet\n", encoding="utf-8")
        code, out, err = self._check()
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("---", err)
        self.assertIn(str(self.golden), err)

    def test_missing_golden_exits_one_with_clear_error(self):
        code, out, err = self._check()
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("no golden packet", err)
        self.assertIn(str(self.golden), err)


if __name__ == "__main__":
    unittest.main()
