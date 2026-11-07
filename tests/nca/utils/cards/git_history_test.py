# Unit tests for prosoc.nca.utils.cards.git_history.
#
# Uses disposable, throwaway git repos created fresh inside each test (never
# the real prosoc repo) -- a repo created by `git init` in a temp dir has its
# own complete history from commit zero, so these tests are unaffected by
# this checkout's own history or clone depth.

import subprocess
import tempfile
import unittest
from pathlib import Path

from prosoc.nca.utils.cards import git_history


def _run(args: list[str], cwd: Path) -> None:
    subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)


def _init_repo(root: Path) -> None:
    _run(["git", "init", "-q"], root)
    _run(["git", "config", "user.email", "test@example.com"], root)
    _run(["git", "config", "user.name", "Test"], root)


def _commit_all(root: Path, message: str) -> None:
    _run(["git", "add", "-A"], root)
    _run(["git", "commit", "-q", "-m", message], root)


class AuditReferenceTextTest(unittest.TestCase):
    def test_returns_card_content_as_of_the_audit_commit(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _init_repo(root)
            card = root / "card.md"
            audit = root / "audit.md"
            card.write_text("version 1\n", encoding="utf-8")
            audit.write_text("verdict: ready\n", encoding="utf-8")
            _commit_all(root, "initial")

            # A later, uncommitted-at-audit-time change to the card.
            card.write_text("version 2\n", encoding="utf-8")
            _commit_all(root, "edit card only")

            text = git_history.audit_reference_text(audit, card)
            self.assertEqual(text, "version 1\n")

    def test_returns_none_when_audit_md_has_uncommitted_changes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _init_repo(root)
            card = root / "card.md"
            audit = root / "audit.md"
            card.write_text("version 1\n", encoding="utf-8")
            audit.write_text("verdict: ready\n", encoding="utf-8")
            _commit_all(root, "initial")

            # Mid-edit: a fresh audit.md rewrite, not yet committed.
            audit.write_text("verdict: ready_with_fixes\n", encoding="utf-8")

            self.assertIsNone(git_history.audit_reference_text(audit, card))

    def test_returns_none_when_audit_md_is_untracked(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _init_repo(root)
            card = root / "card.md"
            audit = root / "audit.md"
            card.write_text("version 1\n", encoding="utf-8")
            _commit_all(root, "card only")
            # audit.md exists on disk but was never committed.
            audit.write_text("verdict: ready\n", encoding="utf-8")

            self.assertIsNone(git_history.audit_reference_text(audit, card))

    def test_returns_none_when_audit_md_has_no_history(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _init_repo(root)
            card = root / "card.md"
            card.write_text("version 1\n", encoding="utf-8")
            _commit_all(root, "card only")
            # No audit.md at all -- git log finds nothing for it.
            audit = root / "audit.md"

            self.assertIsNone(git_history.audit_reference_text(audit, card))

    def test_returns_none_outside_a_git_repository(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            card = root / "card.md"
            audit = root / "audit.md"
            card.write_text("version 1\n", encoding="utf-8")
            audit.write_text("verdict: ready\n", encoding="utf-8")
            # No `git init` at all.

            self.assertIsNone(git_history.audit_reference_text(audit, card))

    def test_returns_none_when_card_did_not_exist_at_the_audit_commit(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _init_repo(root)
            audit = root / "audit.md"
            audit.write_text("verdict: ready\n", encoding="utf-8")
            _commit_all(root, "audit only")

            # The card is added later, in a commit after the audit commit.
            card = root / "card.md"
            card.write_text("version 1\n", encoding="utf-8")
            _commit_all(root, "add card")

            self.assertIsNone(git_history.audit_reference_text(audit, card))

    def test_unaffected_by_later_commits_touching_only_the_card(self):
        # The reference point tracks the *audit*'s last commit, not the
        # card's -- further card-only edits after the audit must not move
        # the reference point.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _init_repo(root)
            card = root / "card.md"
            audit = root / "audit.md"
            card.write_text("version 1\n", encoding="utf-8")
            audit.write_text("verdict: ready\n", encoding="utf-8")
            _commit_all(root, "initial")

            card.write_text("version 2\n", encoding="utf-8")
            _commit_all(root, "edit 1")
            card.write_text("version 3\n", encoding="utf-8")
            _commit_all(root, "edit 2")

            text = git_history.audit_reference_text(audit, card)
            self.assertEqual(text, "version 1\n")


if __name__ == "__main__":
    unittest.main()
