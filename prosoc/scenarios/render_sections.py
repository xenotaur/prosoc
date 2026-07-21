"""
Scenario section renderer.

This module mechanically renders the `template.md`-required "Scenario Card
Summary" and "Scenario Usage Guide" prose sections into a scenario's
`scenario.md`, sourced from its already-distilled `scenario.yml`. Any field
not yet present in the YAML is never fabricated — it is listed in a trailing
"Remaining gaps" section instead.

It supports the same directory/flat layouts as `prosoc.scenarios.distill`
and reuses that module's discovery and freshness-checking building blocks.
"""

from __future__ import annotations

import argparse
import datetime
import pathlib
import re
from typing import Any

from prosoc.literate import compiler
from prosoc.literate import errors
from prosoc.literate import utils
from prosoc.scenarios import distill


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

SCHEMA_PATH = distill.SCHEMA_PATH
DEFAULT_ROOT_KEY = distill.DEFAULT_ROOT_KEY

CARD_SUMMARY_HEADER = "## Scenario Card Summary"
USAGE_GUIDE_HEADER = "## Scenario Usage Guide"
OVERVIEW_HEADER = "## Scenario Overview"
NOTES_HEADER = "## Notes for Scenario Designers and Evaluators"

_MISSING = object()

# (display label, dotted path into the compiled scenario.yml document)
CARD_SUMMARY_FIELDS: list[tuple[str, tuple[str, ...]]] = [
    ("Scenario Name", ("name",)),
    ("Scenario Description", ("summary",)),
    ("Scientific Purpose", ("scientific_purpose",)),
    ("Physical Environment", ("context", "environment", "type")),
    ("Geometric Layout", ("geometric_layout",)),
    ("Robot Role", ("agents", "robot", "role")),
    ("Robot Task", ("intended_robot_task",)),
    ("Human Behavior", ("intended_human_behavior",)),
    ("Success Metrics", ("scenario_usage_guide", "success_metrics")),
    ("Quality Metrics", ("scenario_usage_guide", "quality_metrics")),
    ("Ideal Outcome", ("ideal_outcome",)),
    ("Related Scenarios", ("related_scenarios",)),
    ("Cited In", ("cited_in",)),
]

CARD_SUMMARY_UNSUPPORTED: tuple[str, ...] = ()

USAGE_GUIDE_FIELDS: list[tuple[str, tuple[str, ...]]] = [
    ("Success Metrics", ("scenario_usage_guide", "success_metrics")),
    ("Quality Metrics", ("scenario_usage_guide", "quality_metrics")),
    ("Ideal Outcome", ("ideal_outcome",)),
    ("Failure Modes", ("scenario_usage_guide", "failure_modes")),
    ("Labeling Criteria", ("scenario_usage_guide", "labeling_criteria")),
]

_EDITED_LINE_RE = re.compile(r"^- \*\*EDITED:\*\* .*$", re.MULTILINE)
_DRAFTED_LINE_RE = re.compile(r"^- \*\*DRAFTED:\*\* .*$", re.MULTILINE)


# -----------------------------------------------------------------------------
# Errors
# -----------------------------------------------------------------------------


class SectionAlreadyPresentError(errors.LiterateError):
    """Raised when a target section already exists in scenario.md."""

    pass


class StaleScenarioYamlError(errors.LiterateError):
    """Raised when scenario.yml doesn't match scenario.md's embedded YAML."""

    pass


# -----------------------------------------------------------------------------
# Field lookup and rendering
# -----------------------------------------------------------------------------


def _lookup(data: dict[str, Any], path: tuple[str, ...]) -> Any:
    """Look up a dotted path in a compiled scenario document.

    Returns `_MISSING` if any segment is absent, or if the resolved value is
    empty (None, "", or []) — an empty value carries no renderable content.
    """
    node: Any = data
    for key in path:
        if not isinstance(node, dict) or key not in node:
            return _MISSING
        node = node[key]

    if isinstance(node, str):
        # YAML folded/literal block scalars (e.g. `summary: >`) commonly
        # carry a trailing newline that would otherwise break bullet
        # rendering onto a stray blank line.
        node = node.strip()

    if node is None or node == "" or node == []:
        return _MISSING
    return node


def _render_field_bullet(label: str, value: Any) -> str:
    if isinstance(value, list):
        lines = [f"- **{label}:**"]
        lines.extend(f"  - {item}" for item in value)
        return "\n".join(lines)
    return f"- **{label}:** {value}"


def _render_section(
    header: str,
    fields: list[tuple[str, tuple[str, ...]]],
    data: dict[str, Any],
    *,
    unsupported: tuple[str, ...] = (),
) -> str:
    lines = [header, ""]
    gaps: list[str] = []

    for label, path in fields:
        value = _lookup(data, path)
        if value is _MISSING:
            gaps.append(label)
        else:
            lines.append(_render_field_bullet(label, value))

    gaps.extend(unsupported)

    if gaps:
        if len(lines) > 2:
            lines.append("")
        lines.append("**Remaining gaps:**")
        lines.append("")
        lines.extend(f"- **{label}** — should-fill-in-now" for label in gaps)

    return "\n".join(lines)


# -----------------------------------------------------------------------------
# scenario.md structural helpers
# -----------------------------------------------------------------------------


def _has_section(text: str, header: str) -> bool:
    pattern = re.compile(rf"^{re.escape(header)}\s*$", re.MULTILINE)
    return pattern.search(text) is not None


def _insert_before(
    text: str,
    anchor_header: str,
    content: str,
    md_path: pathlib.Path,
    *,
    fallback_append: bool = False,
) -> str:
    """Insert `content` as its own section immediately before `anchor_header`.

    If the anchor heading can't be found, either append `content` at the end
    of the document (when `fallback_append` is set, for sections `template.md`
    marks optional) or refuse rather than guess at a placement.
    """
    anchor_re = re.compile(rf"^{re.escape(anchor_header)}\s*$", re.MULTILINE)
    match = anchor_re.search(text)

    if match is None:
        if fallback_append:
            body = text if text.endswith("\n") else text + "\n"
            return f"{body}\n---\n\n{content}\n"
        raise errors.LiterateStructureError(
            f"{md_path} does not contain the expected '{anchor_header}' "
            "heading; cannot locate insertion point"
        )

    insert_at = match.start()
    return f"{text[:insert_at]}{content}\n\n---\n\n{text[insert_at:]}"


def _stamp_edited(text: str, *, edited_by: str, edited_date: str) -> str:
    stamp = f"- **EDITED:** {edited_by}, {edited_date}"

    if _EDITED_LINE_RE.search(text):
        return _EDITED_LINE_RE.sub(stamp, text, count=1)

    match = _DRAFTED_LINE_RE.search(text)
    if match is None:
        raise errors.LiterateStructureError(
            "Could not locate a Status block DRAFTED/EDITED line to stamp"
        )
    return f"{text[:match.end()]}\n{stamp}{text[match.end():]}"


# -----------------------------------------------------------------------------
# Freshness check
# -----------------------------------------------------------------------------


def _load_and_check_freshness(
    source: distill.ScenarioSource,
    schema_path: pathlib.Path,
) -> dict[str, Any]:
    """Recompile scenario.md's embedded YAML and confirm it matches
    scenario.yml on disk, mirroring distill.py's own compile pipeline.

    Returns the compiled document on success.
    """
    compiled = compiler.compile_file(
        md_path=source.md_path,
        schema_path=schema_path,
        root_key=DEFAULT_ROOT_KEY,
    )
    expected_yaml = utils.dump_yaml(compiled)

    if not source.yml_path.exists():
        raise StaleScenarioYamlError(
            f"{source.yml_path} does not exist; run distill.py first"
        )

    actual_yaml = source.yml_path.read_text(encoding="utf-8")
    if actual_yaml != expected_yaml:
        raise StaleScenarioYamlError(
            f"{source.yml_path} is stale relative to {source.md_path}'s "
            "embedded YAML; run distill.py first"
        )

    return compiled


# -----------------------------------------------------------------------------
# Rendering entry point
# -----------------------------------------------------------------------------


def render_scenario_sections(
    source: distill.ScenarioSource,
    *,
    schema_path: pathlib.Path = SCHEMA_PATH,
    dry_run: bool = False,
    show_diffs: bool = False,
    edited_by: str = "render_sections.py",
    edited_date: str | None = None,
) -> None:
    """Render both sections into a single scenario's scenario.md.

    Raises:
        StaleScenarioYamlError: if scenario.yml doesn't match scenario.md's
            embedded YAML (or doesn't exist).
        SectionAlreadyPresentError: if either target section already exists.
        prosoc.literate.errors.LiterateStructureError: if a required
            insertion anchor heading is missing from scenario.md.
    """
    text = source.md_path.read_text(encoding="utf-8")

    present = [
        header
        for header in (CARD_SUMMARY_HEADER, USAGE_GUIDE_HEADER)
        if _has_section(text, header)
    ]
    if present:
        raise SectionAlreadyPresentError(
            f"{source.md_path} already has {', '.join(present)}; skipping"
        )

    compiled = _load_and_check_freshness(source, schema_path)

    card_summary = _render_section(
        CARD_SUMMARY_HEADER,
        CARD_SUMMARY_FIELDS,
        compiled,
        unsupported=CARD_SUMMARY_UNSUPPORTED,
    )
    usage_guide = _render_section(USAGE_GUIDE_HEADER, USAGE_GUIDE_FIELDS, compiled)

    text = _insert_before(text, OVERVIEW_HEADER, card_summary, source.md_path)
    text = _insert_before(
        text, NOTES_HEADER, usage_guide, source.md_path, fallback_append=True
    )
    text = _stamp_edited(
        text,
        edited_by=edited_by,
        edited_date=edited_date or datetime.date.today().isoformat(),
    )

    utils.atomic_write(
        path=source.md_path,
        content=text,
        dry_run=dry_run,
        show_diffs=show_diffs,
    )


# -----------------------------------------------------------------------------
# High-level / batch entry point
# -----------------------------------------------------------------------------


def render_all(
    *,
    root: pathlib.Path,
    layout: str = "directory",
    dry_run: bool = False,
    show_diffs: bool = False,
    scenario: str | None = None,
) -> None:
    schema_path = SCHEMA_PATH

    sources = distill.discover_scenarios(root, layout, scenario=scenario)
    if not sources:
        if scenario is not None:
            raise errors.LiterateDiscoveryError(
                f"No scenario '{scenario}' found under {root}"
            )
        raise errors.LiterateDiscoveryError(f"No scenarios found under {root}")

    for source in sources:
        try:
            render_scenario_sections(
                source,
                schema_path=schema_path,
                dry_run=dry_run,
                show_diffs=show_diffs,
            )
        except (
            SectionAlreadyPresentError,
            StaleScenarioYamlError,
            errors.LiterateStructureError,
        ) as exc:
            print(f"skip {source.md_path}: {exc}")


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Render Scenario Card Summary / Scenario Usage Guide sections "
            "into scenario.md from scenario.yml"
        )
    )
    parser.add_argument(
        "scenario",
        nargs="?",
        default=None,
        help="Scenario id (directory/file name) to render",
    )
    parser.add_argument(
        "--all", action="store_true", help="Render every discovered scenario"
    )
    parser.add_argument(
        "--layout",
        choices=["directory", "flat"],
        default="directory",
        help="Scenario layout style",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show-diffs", action="store_true")

    args = parser.parse_args()

    if args.all == (args.scenario is not None):
        parser.error("Provide exactly one of a scenario id or --all")

    root = pathlib.Path(__file__).parent

    render_all(
        root=root,
        layout=args.layout,
        dry_run=args.dry_run,
        show_diffs=args.show_diffs,
        scenario=None if args.all else args.scenario,
    )


if __name__ == "__main__":
    main()
