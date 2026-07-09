# Unit tests for prosoc.scenarios.distill

import tempfile
import unittest
from pathlib import Path

from prosoc.literate import errors
from prosoc.scenarios import distill


def _make_directory_scenario(root: Path, name: str) -> None:
    scenario_dir = root / name
    scenario_dir.mkdir()
    (scenario_dir / "scenario.md").write_text("# placeholder\n", encoding="utf-8")


def _make_flat_scenario(root: Path, name: str) -> None:
    (root / f"{name}.md").write_text("# placeholder\n", encoding="utf-8")


class TestDiscoverDirectoryLayout(unittest.TestCase):

    def test_scenario_filter_matches_one_of_several(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_directory_scenario(root, "blind_corner_01")
            _make_directory_scenario(root, "leading_01")
            _make_directory_scenario(root, "following_01")

            sources = list(
                distill.discover_directory_layout(root, scenario="leading_01")
            )

            self.assertEqual(len(sources), 1)
            self.assertEqual(sources[0].md_path, root / "leading_01" / "scenario.md")

    def test_scenario_filter_no_match_returns_empty(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_directory_scenario(root, "blind_corner_01")

            sources = list(
                distill.discover_directory_layout(root, scenario="nonexistent")
            )

            self.assertEqual(sources, [])

    def test_no_filter_returns_all(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_directory_scenario(root, "blind_corner_01")
            _make_directory_scenario(root, "leading_01")

            sources = list(distill.discover_directory_layout(root))

            self.assertEqual(len(sources), 2)


class TestDiscoverFlatLayout(unittest.TestCase):

    def test_scenario_filter_matches_by_stem(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_flat_scenario(root, "blind_corner_01")
            _make_flat_scenario(root, "leading_01")

            sources = list(
                distill.discover_flat_layout(root, scenario="blind_corner_01")
            )

            self.assertEqual(len(sources), 1)
            self.assertEqual(sources[0].md_path, root / "blind_corner_01.md")

    def test_scenario_filter_no_match_returns_empty(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_flat_scenario(root, "blind_corner_01")

            sources = list(distill.discover_flat_layout(root, scenario="nonexistent"))

            self.assertEqual(sources, [])


class TestDistillAllScenarioScoping(unittest.TestCase):

    def test_no_match_raises_discovery_error_naming_scenario_and_root(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_directory_scenario(root, "blind_corner_01")

            with self.assertRaises(errors.LiterateDiscoveryError) as ctx:
                distill.distill_all(root=root, scenario="nonexistent")

            message = str(ctx.exception)
            self.assertIn("nonexistent", message)
            self.assertIn(str(root), message)

    def test_empty_corpus_without_scenario_filter_raises_distinct_message(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)

            with self.assertRaises(errors.LiterateDiscoveryError) as ctx:
                distill.distill_all(root=root)

            message = str(ctx.exception)
            self.assertNotIn("nonexistent", message)
            self.assertIn(str(root), message)


if __name__ == "__main__":
    unittest.main()
