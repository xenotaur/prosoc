# Integration tests for prosoc.packet.cli against the sample manifest.

import contextlib
import io
import unittest

import yaml

from prosoc.packet import cli
from prosoc.packet.assemble import PREDICATE_TYPE
from prosoc.packet.loader import REPO_ROOT

SAMPLE = REPO_ROOT / "prosoc" / "manifests" / "sample_packet" / "manifest.yml"


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


if __name__ == "__main__":
    unittest.main()
