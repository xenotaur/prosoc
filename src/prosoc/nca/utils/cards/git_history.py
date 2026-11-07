"""Minimal git-history helper for the audit-currency check.

Used by ``prosoc.nca.utils.cards.validate_status`` to find a card's
Markdown content as of the commit that last touched its sibling
``audit.md``, so :func:`prosoc.nca.utils.cards.status.check_audit_currency`
can compare that reference against the card's current content. Isolated
here so the comparison logic in ``status.py`` stays pure (no subprocess
calls), and so this module alone is what a test needs to fake or point at
a disposable repo.
"""

from __future__ import annotations

import os
import pathlib
import subprocess


def audit_reference_text(
    audit_path: pathlib.Path, card_path: pathlib.Path
) -> str | None:
    """Return ``card_path``'s content as of the last commit that touched
    ``audit_path``, or ``None`` if no reliable reference point exists.

    Returns ``None`` (rather than raising) when: ``audit_path`` has
    uncommitted changes or is untracked (no stable reference point yet —
    mid-edit), the path isn't inside a git repository, ``audit_path`` has
    no commit history at all, ``card_path`` didn't exist at that commit
    (e.g. it was renamed since), the ``git`` executable itself can't be
    found on ``PATH``, or the found commit sits at a **shallow-clone
    boundary** (see below). A caller treats ``None`` as "skip this check"
    per :func:`status.check_audit_currency`'s own contract — never as
    evidence of staleness; this function must never raise for any of
    these cases, since it runs unconditionally for every card
    ``_check_extras`` visits, including ones well below ``AUDITED`` that
    never look at the result.

    **Shallow-clone boundary check.** In a shallow clone (e.g. this
    machine's default ``actions/checkout`` depth of 1), ``git log --
    <path>`` can misattribute the shallow boundary commit as the last
    commit that touched ``<path>``, even when it never did — git has no
    parent-chain information before the cut, so it cannot tell. Verified
    empirically against a real shallow clone: a 3-commit history where
    only commit 1 touched ``audit.md`` and commits 2-3 touched only the
    card, cloned with ``--depth 1``, reports commit 3 (today's `git log`
    HEAD, the shallow boundary) as audit.md's last-touching commit — which
    would silently compare the card's *current* content against itself,
    defeating the guard entirely. Boundary commits are listed verbatim,
    one per line, in ``<git-dir>/shallow``; if the found commit is one of
    them, the result is unreliable and treated the same as "no history".
    """
    cwd = audit_path.parent
    audit_name = audit_path.name
    card_rel = os.path.relpath(card_path, cwd)

    try:
        dirty = subprocess.run(
            ["git", "status", "--porcelain", "--", audit_name],
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        if dirty.returncode != 0 or dirty.stdout.strip():
            return None

        log = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", audit_name],
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        sha = log.stdout.strip()
        if log.returncode != 0 or not sha:
            return None

        if sha in _shallow_boundary_commits(cwd):
            return None

        show = subprocess.run(
            ["git", "show", f"{sha}:./{card_rel}"],
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        if show.returncode != 0:
            return None
        return show.stdout
    except OSError:
        # git isn't on PATH, or some other OS-level failure launching it.
        return None


def _shallow_boundary_commits(cwd: pathlib.Path) -> set[str]:
    """Return the shallow-clone boundary commit SHAs for the repo at
    ``cwd``, or an empty set if the repo isn't shallow (the common case)
    or its git-dir can't be determined.
    """
    try:
        git_dir = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        if git_dir.returncode != 0:
            return set()
        shallow_file = cwd / git_dir.stdout.strip() / "shallow"
        if not shallow_file.is_file():
            return set()
        return {
            line.strip()
            for line in shallow_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    except OSError:
        return set()
