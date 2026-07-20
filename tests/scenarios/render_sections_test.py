# Unit tests for prosoc.scenarios.render_sections

import tempfile
import unittest
from pathlib import Path

from prosoc.literate import compiler
from prosoc.literate import errors
from prosoc.literate import utils
from prosoc.scenarios import distill
from prosoc.scenarios import render_sections

FULL_YAML = """\
id: full_scenario_01
name: Full Scenario
summary: >
  A robot and a human interact in a fully-specified scenario.
scientific_purpose: pedestrian interaction
geometric_layout: open space
context:
  environment:
    type: indoor
agents:
  robot:
    role: navigating_agent
intended_robot_task: navigate from A to B
intended_human_behavior: cross navigate
ideal_outcome: no collision, smooth crossing
scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
  quality_metrics:
    - P2
  failure_modes:
    - collision with human
  labeling_criteria:
    - outcome labeled success or failure
"""

PARTIAL_YAML = """\
id: partial_scenario_01
name: Partial Scenario
summary: A robot and a human interact in a partially-specified scenario.
context:
  environment:
    type: indoor
agents:
  robot:
    role: navigating_agent
scenario_usage_guide:
  success_metrics:
    - SR
"""


def _scenario_markdown(yaml_body: str, *, extra_sections: bool = True) -> str:
    body = f"""# Scenario: Test Scenario

## Status

- **STATE:** DRAFTED
- **SOURCE:** unit test fixture
- **DRAFTED:** test, 2026-01-01
- **EDITED:** —

---

## Scenario Overview

Placeholder overview prose.

---

## Scenario Specification (Machine-Readable)

```yaml
{yaml_body}```
"""
    if extra_sections:
        body += """
---

## Notes for Scenario Designers and Evaluators

Placeholder notes.
"""
    return body


def _write_scenario(
    root: Path,
    name: str,
    *,
    yaml_body: str,
    stale: bool = False,
    write_yml: bool = True,
    extra_sections: bool = True,
) -> distill.ScenarioSource:
    scenario_dir = root / name
    scenario_dir.mkdir()
    md_path = scenario_dir / "scenario.md"
    yml_path = scenario_dir / "scenario.yml"

    md_path.write_text(
        _scenario_markdown(yaml_body, extra_sections=extra_sections), encoding="utf-8"
    )

    if write_yml:
        if stale:
            yml_path.write_text(
                "id: stale\nname: Stale\nsummary: out of date\n", encoding="utf-8"
            )
        else:
            compiled = compiler.compile_file(
                md_path=md_path,
                schema_path=render_sections.SCHEMA_PATH,
                root_key=render_sections.DEFAULT_ROOT_KEY,
            )
            yml_path.write_text(utils.dump_yaml(compiled), encoding="utf-8")

    return distill.ScenarioSource(md_path=md_path, yml_path=yml_path)


class TestRenderFullyPopulatedScenario(unittest.TestCase):

    def test_renders_both_sections_with_no_gaps(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(root, "full_scenario", yaml_body=FULL_YAML)

            render_sections.render_scenario_sections(source, edited_date="2026-07-19")

            text = source.md_path.read_text(encoding="utf-8")

            self.assertIn(render_sections.CARD_SUMMARY_HEADER, text)
            self.assertIn(render_sections.USAGE_GUIDE_HEADER, text)
            self.assertIn("- **Scenario Name:** Full Scenario", text)
            self.assertIn("- **Success Metrics:**\n  - SR\n  - NoCollisions", text)
            self.assertIn("- **EDITED:** render_sections.py, 2026-07-19", text)

            # A folded YAML scalar's trailing newline must not leak into the
            # rendered bullet as a stray blank line.
            self.assertIn(
                "- **Scenario Description:** A robot and a human interact in "
                "a fully-specified scenario.\n- **Scientific Purpose:**",
                text,
            )

            # Every schema-backed field is present; the only gaps are the two
            # fields with no schema.json counterpart at all (always a gap,
            # by design, regardless of how complete the YAML is).
            self.assertIn("- **Related Scenarios** — should-fill-in-now", text)
            self.assertIn("- **Cited In** — should-fill-in-now", text)
            usage_guide_text = text[text.index(render_sections.USAGE_GUIDE_HEADER) :]
            self.assertNotIn("Remaining gaps", usage_guide_text)

    def test_card_summary_inserted_before_overview_and_usage_guide_before_notes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(root, "full_scenario", yaml_body=FULL_YAML)

            render_sections.render_scenario_sections(source, edited_date="2026-07-19")

            text = source.md_path.read_text(encoding="utf-8")
            self.assertLess(
                text.index(render_sections.CARD_SUMMARY_HEADER),
                text.index(render_sections.OVERVIEW_HEADER),
            )
            self.assertLess(
                text.index(render_sections.USAGE_GUIDE_HEADER),
                text.index(render_sections.NOTES_HEADER),
            )

    def test_dry_run_does_not_modify_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(root, "full_scenario", yaml_body=FULL_YAML)
            original = source.md_path.read_text(encoding="utf-8")

            render_sections.render_scenario_sections(source, dry_run=True)

            self.assertEqual(source.md_path.read_text(encoding="utf-8"), original)


class TestRenderPartialScenario(unittest.TestCase):

    def test_renders_correct_gaps_checklist_without_fabricating(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(root, "partial_scenario", yaml_body=PARTIAL_YAML)

            render_sections.render_scenario_sections(source, edited_date="2026-07-19")

            text = source.md_path.read_text(encoding="utf-8")

            # Populated fields render normally.
            self.assertIn("- **Scenario Name:** Partial Scenario", text)
            self.assertIn("- **Robot Role:** navigating_agent", text)

            # Absent fields are listed as gaps, never invented.
            self.assertIn("- **Scientific Purpose** — should-fill-in-now", text)
            self.assertIn("- **Geometric Layout** — should-fill-in-now", text)
            self.assertIn("- **Ideal Outcome** — should-fill-in-now", text)
            self.assertIn("- **Robot Task** — should-fill-in-now", text)
            self.assertIn("- **Human Behavior** — should-fill-in-now", text)
            self.assertIn("- **Quality Metrics** — should-fill-in-now", text)
            self.assertIn("- **Failure Modes** — should-fill-in-now", text)
            self.assertIn("- **Labeling Criteria** — should-fill-in-now", text)

            # Fields with no schema.json counterpart are always gaps.
            self.assertIn("- **Related Scenarios** — should-fill-in-now", text)
            self.assertIn("- **Cited In** — should-fill-in-now", text)

            self.assertNotIn("Scientific Purpose:**", text.split("Remaining gaps")[0])


class TestRefuseOnExistingSection(unittest.TestCase):

    def test_refuses_when_card_summary_already_present(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(root, "full_scenario", yaml_body=FULL_YAML)
            existing = source.md_path.read_text(encoding="utf-8").replace(
                "## Scenario Overview",
                "## Scenario Card Summary\n\n- **Scenario Name:** Full Scenario\n\n---\n\n## Scenario Overview",
            )
            source.md_path.write_text(existing, encoding="utf-8")

            with self.assertRaises(render_sections.SectionAlreadyPresentError):
                render_sections.render_scenario_sections(source)

    def test_refuses_when_usage_guide_already_present(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(root, "full_scenario", yaml_body=FULL_YAML)
            existing = source.md_path.read_text(encoding="utf-8").replace(
                "## Notes for Scenario Designers and Evaluators",
                "## Scenario Usage Guide\n\n### Success Metrics\n- SR\n\n---\n\n"
                "## Notes for Scenario Designers and Evaluators",
            )
            source.md_path.write_text(existing, encoding="utf-8")

            with self.assertRaises(render_sections.SectionAlreadyPresentError):
                render_sections.render_scenario_sections(source)

    def test_existing_section_check_short_circuits_before_freshness_check(self):
        # A scenario.yml that is stale (or missing) shouldn't matter if the
        # sections are already present: refusing to overwrite is a purely
        # prose-level decision and should win over a compile-and-compare
        # freshness check the renderer would never need to run.
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(
                root, "full_scenario", yaml_body=FULL_YAML, stale=True
            )
            existing = source.md_path.read_text(encoding="utf-8").replace(
                "## Scenario Overview",
                "## Scenario Card Summary\n\n- **Scenario Name:** Full Scenario\n\n---\n\n## Scenario Overview",
            )
            source.md_path.write_text(existing, encoding="utf-8")

            with self.assertRaises(render_sections.SectionAlreadyPresentError):
                render_sections.render_scenario_sections(source)


class TestRefuseOnStaleYaml(unittest.TestCase):

    def test_refuses_when_yaml_out_of_sync(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(
                root, "full_scenario", yaml_body=FULL_YAML, stale=True
            )

            with self.assertRaises(render_sections.StaleScenarioYamlError):
                render_sections.render_scenario_sections(source)

    def test_refuses_when_yaml_missing(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(
                root, "full_scenario", yaml_body=FULL_YAML, write_yml=False
            )

            with self.assertRaises(render_sections.StaleScenarioYamlError):
                render_sections.render_scenario_sections(source)


class TestMissingInsertionAnchor(unittest.TestCase):

    def test_missing_notes_header_falls_back_to_append(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(
                root, "full_scenario", yaml_body=FULL_YAML, extra_sections=False
            )

            render_sections.render_scenario_sections(source, edited_date="2026-07-19")

            text = source.md_path.read_text(encoding="utf-8")
            self.assertIn(render_sections.USAGE_GUIDE_HEADER, text)

    def test_missing_overview_header_raises_structure_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(root, "full_scenario", yaml_body=FULL_YAML)
            broken = source.md_path.read_text(encoding="utf-8").replace(
                "## Scenario Overview", "## Overview"
            )
            source.md_path.write_text(broken, encoding="utf-8")
            compiled = compiler.compile_file(
                md_path=source.md_path,
                schema_path=render_sections.SCHEMA_PATH,
                root_key=render_sections.DEFAULT_ROOT_KEY,
            )
            source.yml_path.write_text(utils.dump_yaml(compiled), encoding="utf-8")

            with self.assertRaises(errors.LiterateStructureError):
                render_sections.render_scenario_sections(source)


class TestRenderAll(unittest.TestCase):

    def test_no_match_raises_discovery_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_scenario(root, "full_scenario", yaml_body=FULL_YAML)

            with self.assertRaises(errors.LiterateDiscoveryError):
                render_sections.render_all(root=root, scenario="nonexistent")

    def test_all_scopes_to_single_scenario(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(root, "full_scenario", yaml_body=FULL_YAML)
            _write_scenario(root, "another_scenario", yaml_body=FULL_YAML)

            render_sections.render_all(root=root, scenario="full_scenario")

            self.assertIn(
                render_sections.CARD_SUMMARY_HEADER,
                source.md_path.read_text(encoding="utf-8"),
            )
            other_text = (root / "another_scenario" / "scenario.md").read_text(
                encoding="utf-8"
            )
            self.assertNotIn(render_sections.CARD_SUMMARY_HEADER, other_text)

    def test_all_batch_skips_already_present_without_raising(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(root, "full_scenario", yaml_body=FULL_YAML)
            existing = source.md_path.read_text(encoding="utf-8").replace(
                "## Scenario Overview",
                "## Scenario Card Summary\n\n- **Scenario Name:** Full Scenario\n\n---\n\n## Scenario Overview",
            )
            source.md_path.write_text(existing, encoding="utf-8")

            # Should not raise even though this scenario already has a section.
            render_sections.render_all(root=root)

    def test_all_batch_skips_missing_anchor_without_raising(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = _write_scenario(root, "full_scenario", yaml_body=FULL_YAML)
            broken = source.md_path.read_text(encoding="utf-8").replace(
                "## Scenario Overview", "## Overview"
            )
            source.md_path.write_text(broken, encoding="utf-8")
            compiled = compiler.compile_file(
                md_path=source.md_path,
                schema_path=render_sections.SCHEMA_PATH,
                root_key=render_sections.DEFAULT_ROOT_KEY,
            )
            source.yml_path.write_text(utils.dump_yaml(compiled), encoding="utf-8")

            # A structurally non-conforming scenario.md must not crash a
            # batch run; it's reported and skipped like any other refusal.
            render_sections.render_all(root=root)


if __name__ == "__main__":
    unittest.main()
