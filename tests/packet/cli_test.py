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
JUSTIFICATION = "CI packet-drift check (dev-mode golden; corpus not yet APPROVED)"


def _run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()


class CliTest(unittest.TestCase):
    def test_sample_manifest_exists(self):
        self.assertTrue(SAMPLE.exists())

    def test_fail_closed_default_emits_nothing(self):
        # The checked-in corpus is pre-APPROVED, so the default gate blocks and
        # nothing is written to stdout.
        code, out, err = _run([str(SAMPLE)])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("fail-closed", err)

    def test_allow_unapproved_emits_valid_packet(self):
        code, out, err = _run([str(SAMPLE), "--allow-unapproved", "integration test"])
        self.assertEqual(code, 0)
        env = yaml.safe_load(out)
        self.assertEqual(env["predicate_type"], PREDICATE_TYPE)
        self.assertIn("notice", env["guidance"])
        self.assertTrue(env["predicate"]["policy"]["escape_hatch"])

    def test_empty_justification_rejected(self):
        code, _, err = _run([str(SAMPLE), "--allow-unapproved", "   "])
        self.assertEqual(code, 2)
        self.assertIn("justification", err)

    def test_missing_manifest(self):
        code, _, err = _run([str(REPO_ROOT / "nope.yml")])
        self.assertEqual(code, 1)
        self.assertIn("not found", err)

    def test_check_matches_the_checked_in_golden(self):
        code, out, err = _run(
            [str(SAMPLE), "--allow-unapproved", JUSTIFICATION, "--check"]
        )
        self.assertEqual(code, 0)
        self.assertEqual(out, "")
        self.assertEqual(err, "")

    def test_check_rejects_format_json(self):
        code, out, err = _run(
            [
                str(SAMPLE),
                "--allow-unapproved",
                JUSTIFICATION,
                "--check",
                "--format",
                "json",
            ]
        )
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
        return _run(
            [str(self.manifest), "--allow-unapproved", JUSTIFICATION, "--check"]
        )

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
        self.assertIn("+++", err)

    def test_missing_golden_exits_one_with_clear_error(self):
        code, out, err = self._check()
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("no golden packet", err)
        self.assertIn(str(self.golden), err)


if __name__ == "__main__":
    unittest.main()
