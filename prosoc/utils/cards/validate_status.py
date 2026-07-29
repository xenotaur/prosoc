"""CLI: validate card lifecycle-state consistency across families.

Checks that each card's Markdown ``## Status`` / ``## STATUS`` STATE line agrees
with the machine-readable ``state`` field in its distilled ``*.yml``. Exits
non-zero if any card is inconsistent or missing a state.

Family-aware: with no ``--family`` it validates every registered family
(scenarios, tasks, …) over their default repo roots. ``--family NAME`` restricts
to one family and permits ``--root`` / ``--card`` overrides. Run via
``scripts/validate/status`` (a thin wrapper around
``python -m prosoc.utils.cards.validate_status``).
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from dataclasses import dataclass
from typing import Callable

from prosoc.constitutions import distill as constitutions_distill
from prosoc.contexts import distill as contexts_distill
from prosoc.literate import utils
from prosoc.scenarios import distill as scenarios_distill
from prosoc.tasks import distill as tasks_distill
from prosoc.utils.cards import status


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


FAMILIES: dict[str, Family] = {
    "scenarios": Family(
        name="scenarios",
        default_root=pathlib.Path(scenarios_distill.__file__).parent,
        supports_flat=True,
        discover=lambda root, layout: scenarios_distill.discover_scenarios(
            root, layout
        ),
    ),
    "tasks": Family(
        name="tasks",
        default_root=pathlib.Path(tasks_distill.__file__).parent,
        supports_flat=False,
        discover=lambda root, layout: tasks_distill.discover_tasks(root),
    ),
    "contexts": Family(
        name="contexts",
        default_root=pathlib.Path(contexts_distill.__file__).parent,
        supports_flat=False,
        # discover_contexts is a generator; wrap in list() so the caller's
        # len()/`not sources` checks work.
        discover=lambda root, layout: list(contexts_distill.discover_contexts(root)),
    ),
    "constitutions": Family(
        name="constitutions",
        default_root=pathlib.Path(constitutions_distill.__file__).parent,
        # discover_constitutions dispatches on layout and handles flat too.
        supports_flat=True,
        discover=lambda root, layout: constitutions_distill.discover_constitutions(
            root, layout
        ),
        # constitution.yml is root-wrapped: state lives at constitution.state.
        yaml_root_key="constitution",
    ),
}


def _label(source, layout: str) -> str:
    """Card id for display/filtering: file stem in flat layout, else dir name."""
    return source.md_path.stem if layout == "flat" else source.md_path.parent.name


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
        matched = [s for s in sources if _label(s, layout) == card]
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
        name = f"{family.name}/{_label(source, layout)}"
        try:
            result = status.check_source(
                source.md_path, source.yml_path, root_key=family.yaml_root_key
            )
        except status.StatusStateError as exc:
            print(f"FAIL {name}: {exc}", file=sys.stderr)
            failures += 1
            continue

        if result.ok:
            print(f"ok   {name}: {result.detail}")
            continue

        if fix:
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
        else:
            print(f"FAIL {name}: {result.detail}", file=sys.stderr)
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
