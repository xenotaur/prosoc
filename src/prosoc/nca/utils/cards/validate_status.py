"""CLI: validate card lifecycle-state consistency across families.

Checks that each card's Markdown ``## Status`` / ``## STATUS`` STATE line agrees
with the machine-readable ``state`` field in its distilled ``*.yml``. Also
checks (see ``prosoc.nca.utils.cards.status``) that an ``AUDITED``/``APPROVED``
card has real audit evidence (``audit.md`` in directory layout, or a
card-specific ``<stem>.audit.md`` in flat layout, with an acceptable verdict —
not the optional ``AUDITED:`` provenance bullet); that its content hasn't
drifted since that audit evidence was last touched (comparing the card's
Markdown, with the lifecycle-tracking surface masked out, against its git
history — see ``status.check_audit_currency``); and, for the charter
specifically, that its free-text ``**Status:**`` header agrees with its
``STATE``. Exits non-zero if any card fails any of these checks.

Family-aware: with no ``--family`` it validates every registered family
(scenarios, tasks, …) over their default repo roots. ``--family NAME`` restricts
to one family and permits ``--root`` / ``--card`` overrides. Run via
``scripts/validate/status`` (a thin wrapper around
``python -m prosoc.nca.utils.cards.validate_status``).
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from dataclasses import dataclass
from typing import Callable

from prosoc.constitutions import distill as constitutions_distill
from prosoc.manifests import distill as manifests_distill
from prosoc.nca.literate import utils
from prosoc.nca.utils.cards import git_history, status
from prosoc.nca.utils.cards.family_registry import CARD_FAMILIES
from prosoc.prnc.charter import distill as charter_distill
from prosoc.prnc.contexts import distill as contexts_distill
from prosoc.prnc.scenarios import distill as scenarios_distill
from prosoc.prnc.tasks import distill as tasks_distill


@dataclass(frozen=True)
class Family:
    """A card family the status validator knows how to discover and check."""

    name: str
    default_root: pathlib.Path
    supports_flat: bool
    # (root, layout) -> list of sources exposing ``md_path`` / ``yml_path``.
    discover: Callable[[pathlib.Path, str], list]
    # For root-wrapped families whose ``*.yml`` nests the payload (and ``state``)
    # under a top key (e.g. constitutions -> "constitution"); None = top-level.
    yaml_root_key: str | None = None
    # Label/``--card`` id by the Markdown file *stem* rather than its parent
    # directory name. Set for single-source families (e.g. charter) whose card
    # id must stay stable regardless of the ``--root`` directory's name.
    label_by_stem: bool = False


def _family(identity, *, supports_flat: bool, discover) -> Family:
    return Family(
        name=identity.name,
        default_root=identity.root,
        supports_flat=supports_flat,
        discover=discover,
        yaml_root_key=identity.yaml_root_key,
        # The one single-document family (charter) is labeled by its
        # Markdown stem rather than its parent directory name.
        label_by_stem=identity.single,
    )


FAMILIES: dict[str, Family] = {
    "scenarios": _family(
        CARD_FAMILIES["scenarios"],
        supports_flat=True,
        discover=lambda root, layout: scenarios_distill.discover_scenarios(
            root, layout
        ),
    ),
    "tasks": _family(
        CARD_FAMILIES["tasks"],
        supports_flat=False,
        discover=lambda root, layout: tasks_distill.discover_tasks(root),
    ),
    "contexts": _family(
        CARD_FAMILIES["contexts"],
        supports_flat=False,
        # discover_contexts is a generator; wrap in list() so the caller's
        # len()/`not sources` checks work.
        discover=lambda root, layout: list(contexts_distill.discover_contexts(root)),
    ),
    "constitutions": _family(
        CARD_FAMILIES["constitutions"],
        # discover_constitutions dispatches on layout and handles flat too.
        supports_flat=True,
        discover=lambda root, layout: constitutions_distill.discover_constitutions(
            root, layout
        ),
    ),
    "charter": _family(
        CARD_FAMILIES["charter"],
        # The charter is a single document (charter.md -> charter.yml), not a
        # directory/flat layout; discover_charter returns at most one source.
        supports_flat=False,
        discover=lambda root, layout: charter_distill.discover_charter(root),
    ),
    # manifests is validate_status-only -- loader.py has no equivalent, so
    # it isn't part of the shared CARD_FAMILIES registry.
    "manifests": Family(
        name="manifests",
        default_root=pathlib.Path(manifests_distill.__file__).parent,
        supports_flat=False,
        discover=lambda root, layout: manifests_distill.discover_manifests(root),
    ),
}


def _label(source, layout: str, family: Family) -> str:
    """Card id for display/filtering: file stem in flat layout or for
    single-source families (``label_by_stem``), else the parent directory name."""
    if layout == "flat" or family.label_by_stem:
        return source.md_path.stem
    return source.md_path.parent.name


def _check_extras(family: Family, source, layout: str) -> list[str]:
    """Run the audit-evidence check, the audit-currency check (all
    families), and the charter-only Status:-line check. Returns a
    failure-detail string per failing check (empty if all pass).

    Evaluated against the Markdown's *current* STATE line (as it stands on
    disk when this runs, before any ``--fix`` rewrite in this same
    invocation) — these are display-accuracy checks, not an extension of
    the STATE-vs-YAML consistency check above, and ``--fix`` never
    addresses them (it only ever projects the YAML state onto the Markdown
    STATE line).
    """
    try:
        md_text = source.md_path.read_text(encoding="utf-8")
        markdown_state = status.parse_markdown_state(md_text)
    except status.StatusStateError:
        # No STATE line at all; the primary check already reports this.
        return []

    problems = []
    audit_result = status.check_audit_evidence(
        source.md_path, markdown_state, layout=layout
    )
    if not audit_result.ok:
        problems.append(audit_result.detail)

    reference_text = None
    yml_reference_text = None
    current_yml_text = None
    if markdown_state in ("AUDITED", "APPROVED"):
        # check_audit_currency is a no-op below AUDITED; skip the git
        # subprocess calls entirely rather than running them (now doubled,
        # one pass each for the Markdown and the distilled YAML) only to
        # discard the result.
        audit_path = status.audit_path_for(source.md_path, layout=layout)
        reference_text = git_history.audit_reference_text(audit_path, source.md_path)
        yml_reference_text = git_history.audit_reference_text(
            audit_path, source.yml_path
        )
        if yml_reference_text is not None:
            # Only needed for the comparison itself; reading it costs
            # nothing extra when there's no reference point to compare
            # against anyway.
            current_yml_text = source.yml_path.read_text(encoding="utf-8")
    currency_result = status.check_audit_currency(
        current_md_text=md_text,
        audit_reference_md_text=reference_text,
        state=markdown_state,
        yaml_root_key=family.yaml_root_key,
        current_yml_text=current_yml_text,
        audit_reference_yml_text=yml_reference_text,
    )
    if not currency_result.ok:
        problems.append(currency_result.detail)

    if family.name == "charter":
        charter_result = status.check_charter_status_line(md_text, markdown_state)
        if not charter_result.ok:
            problems.append(charter_result.detail)

    return problems


def _check_family(family: Family, root: pathlib.Path, layout: str, card, fix: bool):
    """Return (checked_count, failures) after reporting each card in the family.

    Progress lines (``ok`` / ``fix``) go to stdout; failures go to stderr.
    """
    if layout == "flat" and not family.supports_flat:
        print(
            f"FAIL {family.name}: flat layout is not supported for this family",
            file=sys.stderr,
        )
        return 0, 1

    sources = family.discover(root, layout)
    if card is not None:
        matched = [s for s in sources if _label(s, layout, family) == card]
        if not matched:
            # Distinguish "that card isn't here" from "no cards at all".
            found = "" if not sources else f" (root has other cards under {root})"
            print(
                f"FAIL {family.name}: no card {card!r} found{found}",
                file=sys.stderr,
            )
            return 0, 1
        sources = matched

    if not sources:
        print(f"FAIL {family.name}: no cards found under {root}", file=sys.stderr)
        return 0, 1

    failures = 0
    for source in sources:
        name = f"{family.name}/{_label(source, layout, family)}"
        try:
            result = status.check_source(
                source.md_path, source.yml_path, root_key=family.yaml_root_key
            )
        except status.StatusStateError as exc:
            print(f"FAIL {name}: {exc}", file=sys.stderr)
            failures += 1
            continue

        extra_problems = _check_extras(family, source, layout)

        if result.ok and not extra_problems:
            print(f"ok   {name}: {result.detail}")
            continue

        if not result.ok and fix:
            yaml_state = status.read_yaml_state(
                source.yml_path, root_key=family.yaml_root_key
            )
            # Only project from an authoritative state that is itself valid; an
            # unrecognised YAML state is a failure to report, not to fix
            # (projecting it would raise). Keep going so the run still fails.
            if yaml_state not in status.STATES:
                print(
                    f"FAIL {name}: cannot fix — YAML state {yaml_state!r} "
                    "is not a recognised lifecycle state",
                    file=sys.stderr,
                )
                failures += 1
                continue
            fixed = status.project_state_into_markdown(
                source.md_path.read_text(encoding="utf-8"), yaml_state
            )
            utils.atomic_write(path=source.md_path, content=fixed)
            print(f"fix  {name}: projected Markdown STATE -> {yaml_state}")
            # --fix only ever projects the STATE line; it never addresses an
            # audit-evidence or charter Status:-line gap, so those still fail.
            if extra_problems:
                print(f"FAIL {name}: {'; '.join(extra_problems)}", file=sys.stderr)
                failures += 1
        else:
            details = [] if result.ok else [result.detail]
            details.extend(extra_problems)
            print(f"FAIL {name}: {'; '.join(details)}", file=sys.stderr)
            failures += 1

    return len(sources), failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check card Markdown STATE line vs YAML state field agreement "
            "across families."
        )
    )
    parser.add_argument(
        "--family",
        choices=sorted(FAMILIES),
        default=None,
        help="Restrict to one card family (default: all registered families).",
    )
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=None,
        help="Override the family's card root (requires a single --family).",
    )
    parser.add_argument(
        "--layout",
        choices=["directory", "flat"],
        default="directory",
        help="Card layout style (flat is only supported by some families).",
    )
    parser.add_argument(
        "--card",
        default=None,
        help="Restrict to a single card id/directory name (requires --family).",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help=(
            "Project the Markdown STATE line from the authoritative YAML state "
            "for any inconsistent card, instead of only reporting."
        ),
    )
    args = parser.parse_args(argv)

    families = [FAMILIES[args.family]] if args.family else list(FAMILIES.values())

    if args.root is not None and args.family is None:
        parser.error("--root requires --family (it overrides one family's root)")
    if args.card is not None and args.family is None:
        parser.error("--card requires --family")

    total = 0
    failures = 0
    for family in families:
        root = args.root if args.root is not None else family.default_root
        checked, fam_failures = _check_family(
            family, root, args.layout, args.card, args.fix
        )
        total += checked
        failures += fam_failures

    if failures:
        print(f"\n{failures} card(s) inconsistent or missing.", file=sys.stderr)
        return 1
    print(f"\nAll {total} card(s) consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
