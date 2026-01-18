import unittest
from pathlib import Path

from prosoc.utils.paths import find_repo_root, RepoRootNotFoundError


class TestFindRepoRoot(unittest.TestCase):
    """Unit tests for find_repo_root utility."""

    def test_find_repo_root_from_this_file(self):
        """
        Starting from this test file, find_repo_root should locate
        the repository root containing pyproject.toml.
        """
        repo_root = find_repo_root(start=Path(__file__))

        self.assertTrue((repo_root / "pyproject.toml").exists())

    def test_find_repo_root_from_subdirectory(self):
        """
        Starting from a deeper subdirectory, find_repo_root should
        still locate the same repository root.
        """
        start_path = Path(__file__).parent
        repo_root = find_repo_root(start=start_path)

        self.assertTrue((repo_root / "pyproject.toml").exists())

    def test_find_repo_root_raises_when_not_found(self):
        """
        When no marker file exists within the search depth,
        find_repo_root should raise RepoRootNotFoundError.
        """
        # Use an artificial path that is very unlikely to contain pyproject.toml
        fake_root = Path("/")

        with self.assertRaises(RepoRootNotFoundError):
            find_repo_root(start=fake_root, max_depth=2)


if __name__ == "__main__":
    unittest.main()
