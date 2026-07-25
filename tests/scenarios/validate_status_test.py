# Unit tests for prosoc.scenarios.validate_status CLI

import tempfile
import unittest
from pathlib import Path

from prosoc.scenarios import validate_status


MD_DRAFTED = """\
# Scenario: Example

## Status

- **STATE:** DRAFTED
- **SOURCE:** somewhere

---
"""


def _make_scenario(root: Path, name: str, md_state: str, yml_state: str) -> None:
    d = root / name
    d.mkdir()
    (d / "scenario.md").write_text(
        MD_DRAFTED.replace("DRAFTED", md_state), encoding="utf-8"
    )
    (d / "scenario.yml").write_text(
        f"id: {name}_01\nname: {name}\nstate: {yml_state}\nsummary: y\n",
        encoding="utf-8",
    )


class ValidateStatusCliTest(unittest.TestCase):
    def test_consistent_returns_zero(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _make_scenario(root, "good", "DRAFTED", "DRAFTED")
            self.assertEqual(validate_status.main(["--root", str(root)]), 0)

    def test_inconsistent_returns_one(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _make_scenario(root, "bad", "DRAFTED", "APPROVED")
            self.assertEqual(validate_status.main(["--root", str(root)]), 1)

    def test_fix_projects_markdown_and_then_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _make_scenario(root, "bad", "DRAFTED", "APPROVED")
            # --fix rewrites the Markdown STATE line from the YAML state.
            self.assertEqual(validate_status.main(["--root", str(root), "--fix"]), 0)
            md = (root / "bad" / "scenario.md").read_text(encoding="utf-8")
            self.assertIn("- **STATE:** APPROVED", md)
            # A subsequent plain check now passes.
            self.assertEqual(validate_status.main(["--root", str(root)]), 0)

    def test_empty_root_returns_one(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(validate_status.main(["--root", d]), 1)


if __name__ == "__main__":
    unittest.main()
