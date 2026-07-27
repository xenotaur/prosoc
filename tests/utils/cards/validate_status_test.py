# Unit tests for prosoc.utils.cards.validate_status (family-aware CLI)

import tempfile
import unittest
from pathlib import Path

from prosoc.utils.cards import validate_status

MD = """\
# Card: Example

## Status

- **STATE:** DRAFTED
- **SOURCE:** somewhere

---
"""


def _dir_card(root: Path, name: str, md_state: str, yml_state: str, stem: str) -> None:
    """Directory-layout card: <root>/<name>/<stem>.md and <stem>.yml."""
    d = root / name
    d.mkdir()
    (d / f"{stem}.md").write_text(MD.replace("DRAFTED", md_state), encoding="utf-8")
    (d / f"{stem}.yml").write_text(
        f"id: {name}_01\nname: {name}\nstate: {yml_state}\nsummary: y\n",
        encoding="utf-8",
    )


def _flat_card(root: Path, name: str, md_state: str, yml_state: str) -> None:
    (root / f"{name}.md").write_text(MD.replace("DRAFTED", md_state), encoding="utf-8")
    (root / f"{name}.yml").write_text(
        f"id: {name}_01\nname: {name}\nstate: {yml_state}\nsummary: y\n",
        encoding="utf-8",
    )


class ScenariosFamilyTest(unittest.TestCase):
    def test_consistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "good", "DRAFTED", "DRAFTED", "scenario")
            self.assertEqual(
                validate_status.main(["--family", "scenarios", "--root", str(root)]), 0
            )

    def test_inconsistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "bad", "DRAFTED", "APPROVED", "scenario")
            self.assertEqual(
                validate_status.main(["--family", "scenarios", "--root", str(root)]), 1
            )

    def test_flat_layout(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _flat_card(root, "flat", "EDITED", "EDITED")
            self.assertEqual(
                validate_status.main(
                    ["--family", "scenarios", "--root", str(root), "--layout", "flat"]
                ),
                0,
            )

    def test_fix_projects_then_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "bad", "DRAFTED", "APPROVED", "scenario")
            self.assertEqual(
                validate_status.main(
                    ["--family", "scenarios", "--root", str(root), "--fix"]
                ),
                0,
            )
            self.assertIn(
                "- **STATE:** APPROVED",
                (root / "bad" / "scenario.md").read_text(encoding="utf-8"),
            )

    def test_fix_invalid_yaml_state_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "nope", "DRAFTED", "BOGUS", "scenario")
            self.assertEqual(
                validate_status.main(
                    ["--family", "scenarios", "--root", str(root), "--fix"]
                ),
                1,
            )
            self.assertIn(
                "- **STATE:** DRAFTED",
                (root / "nope" / "scenario.md").read_text(encoding="utf-8"),
            )


class TasksFamilyTest(unittest.TestCase):
    def test_consistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "deliver", "DRAFTED", "DRAFTED", "task")
            self.assertEqual(
                validate_status.main(["--family", "tasks", "--root", str(root)]), 0
            )

    def test_inconsistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "deliver", "DRAFTED", "APPROVED", "task")
            self.assertEqual(
                validate_status.main(["--family", "tasks", "--root", str(root)]), 1
            )

    def test_flat_layout_unsupported_fails(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(
                validate_status.main(
                    ["--family", "tasks", "--root", d, "--layout", "flat"]
                ),
                1,
            )


class GuardsAndDefaultsTest(unittest.TestCase):
    def test_root_requires_family(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(SystemExit):
                validate_status.main(["--root", d])

    def test_card_requires_family(self):
        with self.assertRaises(SystemExit):
            validate_status.main(["--card", "blind_corner"])

    def test_empty_family_root_fails(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(
                validate_status.main(["--family", "scenarios", "--root", d]), 1
            )

    def test_card_no_match_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "present", "DRAFTED", "DRAFTED", "scenario")
            # A --card that matches nothing (while other cards exist) fails.
            self.assertEqual(
                validate_status.main(
                    ["--family", "scenarios", "--root", str(root), "--card", "absent"]
                ),
                1,
            )

    def test_default_all_families_over_real_repo_is_consistent(self):
        # Integration smoke test: the checked-in corpus (scenarios + tasks) must
        # stay consistent. This is the guard the WI's acceptance depends on.
        self.assertEqual(validate_status.main([]), 0)


if __name__ == "__main__":
    unittest.main()
