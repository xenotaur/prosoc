"""CLI: validate scenario lifecycle-state consistency.

Checks that each scenario's Markdown ``## Status`` STATE line agrees with the
machine-readable ``state`` field in its distilled ``scenario.yml``. Exits
non-zero if any scenario is inconsistent or missing a state.

Run via ``scripts/validate/status`` (a thin wrapper around
``python -m prosoc.scenarios.validate_status``), mirroring the distiller CLIs.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

from prosoc.literate import utils
from prosoc.scenarios import distill, status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check scenario Markdown STATE line vs YAML state field agreement."
        )
    )
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=pathlib.Path(distill.__file__).parent,
        help="Scenarios root (default: prosoc/scenarios).",
    )
    parser.add_argument(
        "--layout",
        choices=["directory", "flat"],
        default="directory",
        help="Scenario layout style.",
    )
    parser.add_argument(
        "--scenario",
        default=None,
        help="Restrict to a single scenario id/directory name.",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help=(
            "Project the Markdown STATE line from the authoritative YAML state "
            "for any inconsistent scenario, instead of only reporting."
        ),
    )
    args = parser.parse_args(argv)

    sources = distill.discover_scenarios(args.root, args.layout, scenario=args.scenario)
    if not sources:
        print(f"no scenarios found under {args.root}", file=sys.stderr)
        return 1

    failures = 0
    for source in sources:
        # In directory layout the scenario id is the parent directory name; in
        # flat layout the sources live directly under --root, so the id is the
        # Markdown file stem.
        if args.layout == "flat":
            name = source.md_path.stem
        else:
            name = source.md_path.parent.name

        try:
            result = status.check_source(source.md_path, source.yml_path)
        except status.StatusStateError as exc:
            print(f"FAIL {name}: {exc}")
            failures += 1
            continue

        if result.ok:
            print(f"ok   {name}: {result.detail}")
            continue

        if args.fix:
            yaml_state = status.read_yaml_state(source.yml_path)
            # Only project from an authoritative state that is itself valid;
            # an unrecognised YAML state is a failure to report, not to fix
            # (projecting it would raise). Keep going so the CLI still returns
            # a non-zero status for the run.
            if yaml_state not in status.STATES:
                print(
                    f"FAIL {name}: cannot fix — YAML state {yaml_state!r} "
                    "is not a recognised lifecycle state"
                )
                failures += 1
                continue
            fixed = status.project_state_into_markdown(
                source.md_path.read_text(encoding="utf-8"), yaml_state
            )
            utils.atomic_write(path=source.md_path, content=fixed)
            print(f"fix  {name}: projected Markdown STATE -> {yaml_state}")
        else:
            print(f"FAIL {name}: {result.detail}")
            failures += 1

    if failures:
        print(f"\n{failures} scenario(s) inconsistent.", file=sys.stderr)
        return 1
    print(f"\nAll {len(sources)} scenario(s) consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
