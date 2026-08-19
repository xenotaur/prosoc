# Unit tests for prosoc.nca.utils.cards.validate_status (family-aware CLI)

import tempfile
import unittest
from pathlib import Path

from prosoc.nca.utils.cards import validate_status


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


class ContextsFamilyTest(unittest.TestCase):
    # discover_contexts is a generator; the registry wraps it in list(). These
    # tests exercise the real contexts family via a temp root and so guard that
    # the generator-wrapping keeps the validator's len()/`not sources` logic
    # working (an unwrapped generator would raise or misreport here).

    def test_consistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "routine", "DRAFTED", "DRAFTED", "context")
            self.assertEqual(
                validate_status.main(["--family", "contexts", "--root", str(root)]), 0
            )

    def test_inconsistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "routine", "DRAFTED", "APPROVED", "context")
            self.assertEqual(
                validate_status.main(["--family", "contexts", "--root", str(root)]), 1
            )

    def test_flat_layout_unsupported_fails(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(
                validate_status.main(
                    ["--family", "contexts", "--root", d, "--layout", "flat"]
                ),
                1,
            )


def _constitution_card(root: Path, name: str, md_state: str, yml_state: str) -> None:
    """Constitution card: root-wrapped YAML (state at constitution.state),
    STATUS block with a bold STATE bullet."""
    d = root / name
    d.mkdir()
    (d / "constitution.md").write_text(
        MD.replace("DRAFTED", md_state), encoding="utf-8"
    )
    (d / "constitution.yml").write_text(
        f"constitution:\n  id: {name}\n  name: {name}\n  state: {yml_state}\n",
        encoding="utf-8",
    )


def _flat_constitution_card(
    root: Path, name: str, md_state: str, yml_state: str
) -> None:
    """Flat-layout constitution: <root>/<name>.md and <name>.yml (root-wrapped)."""
    (root / f"{name}.md").write_text(MD.replace("DRAFTED", md_state), encoding="utf-8")
    (root / f"{name}.yml").write_text(
        f"constitution:\n  id: {name}\n  name: {name}\n  state: {yml_state}\n",
        encoding="utf-8",
    )


class ConstitutionsFamilyTest(unittest.TestCase):
    # Constitutions are root-wrapped (state at constitution.state); these tests
    # exercise the Family's yaml_root_key="constitution" path end to end.

    def test_consistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _constitution_card(root, "asimov", "EDITED", "EDITED")
            self.assertEqual(
                validate_status.main(
                    ["--family", "constitutions", "--root", str(root)]
                ),
                0,
            )

    def test_inconsistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _constitution_card(root, "asimov", "EDITED", "APPROVED")
            self.assertEqual(
                validate_status.main(
                    ["--family", "constitutions", "--root", str(root)]
                ),
                1,
            )

    def test_missing_root_wrapper_fails(self):
        # A top-level (non-root-wrapped) YAML must fail for a root-keyed family.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            cd = root / "asimov"
            cd.mkdir()
            (cd / "constitution.md").write_text(
                MD.replace("DRAFTED", "EDITED"), encoding="utf-8"
            )
            (cd / "constitution.yml").write_text(
                "id: asimov\nname: asimov\nstate: EDITED\n", encoding="utf-8"
            )
            self.assertEqual(
                validate_status.main(
                    ["--family", "constitutions", "--root", str(root)]
                ),
                1,
            )

    def test_flat_layout(self):
        # discover_constitutions handles flat layout, so --layout flat is valid.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _flat_constitution_card(root, "asimov", "EDITED", "EDITED")
            self.assertEqual(
                validate_status.main(
                    [
                        "--family",
                        "constitutions",
                        "--root",
                        str(root),
                        "--layout",
                        "flat",
                    ]
                ),
                0,
            )


def _charter_card(root: Path, md_state: str, yml_state: str) -> None:
    """Single-source charter: <root>/charter.md and charter.yml (top-level
    state, sibling of principles)."""
    (root / "charter.md").write_text(MD.replace("DRAFTED", md_state), encoding="utf-8")
    (root / "charter.yml").write_text(
        f"state: {yml_state}\nprinciples:\n- id: P0\n  name: Goal\n",
        encoding="utf-8",
    )


class CharterFamilyTest(unittest.TestCase):
    # The charter is a single-source family (charter.md -> charter.yml) whose
    # state lives at the top level (yaml_root_key=None). discover_charter
    # returns at most one source; these tests exercise that single-source path.

    def test_consistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _charter_card(root, "DRAFTED", "DRAFTED")
            self.assertEqual(
                validate_status.main(["--family", "charter", "--root", str(root)]), 0
            )

    def test_inconsistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _charter_card(root, "DRAFTED", "APPROVED")
            self.assertEqual(
                validate_status.main(["--family", "charter", "--root", str(root)]), 1
            )

    def test_empty_root_fails(self):
        # No charter.md present -> discover_charter returns [] -> "no cards".
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(
                validate_status.main(["--family", "charter", "--root", d]), 1
            )

    def test_card_id_is_stem_not_root_dir_name(self):
        # label_by_stem: --card "charter" must match regardless of the (temp)
        # root directory's name; the card id is the charter.md stem, not the dir.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _charter_card(root, "DRAFTED", "DRAFTED")
            self.assertEqual(
                validate_status.main(
                    ["--family", "charter", "--root", str(root), "--card", "charter"]
                ),
                0,
            )


class ManifestsFamilyTest(unittest.TestCase):
    # manifests is a directory-layout family whose state is non-root-wrapped
    # (yaml_root_key=None), like tasks/contexts — _dir_card's generic
    # id/name/state/summary shape covers the state-consistency check
    # exercised here. Does not support --layout flat (see the test below).

    def test_consistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "sample_packet", "DRAFTED", "DRAFTED", "manifest")
            self.assertEqual(
                validate_status.main(["--family", "manifests", "--root", str(root)]),
                0,
            )

    def test_inconsistent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _dir_card(root, "sample_packet", "DRAFTED", "APPROVED", "manifest")
            self.assertEqual(
                validate_status.main(["--family", "manifests", "--root", str(root)]),
                1,
            )

    def test_flat_layout_unsupported_fails(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(
                validate_status.main(
                    ["--family", "manifests", "--root", d, "--layout", "flat"]
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
