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
    no commit history at all, or ``card_path`` didn't exist at that commit
    (e.g. it was renamed since). A caller treats ``None`` as "skip this
    check" per :func:`status.check_audit_currency`'s own contract — never
    as evidence of staleness.
    """
    cwd = audit_path.parent
    audit_name = audit_path.name
    card_rel = os.path.relpath(card_path, cwd)

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

    show = subprocess.run(
        ["git", "show", f"{sha}:./{card_rel}"],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if show.returncode != 0:
        return None
    return show.stdout
