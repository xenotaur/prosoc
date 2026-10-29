# Regression coverage for the charter supplement's semantic content
# surviving the Markdown -> Pandoc -> LaTeX render pipeline, per
# project/audits/2026-10-26_charter_supplement_pipeline_audit.md and
# WI-CHARTER-SUPPLEMENT-TEST-COVERAGE. Runs real pandoc against the
# real charter-paper source cards (not fakes) -- these tests exist to
# catch a regression in the *real* content, not just the renderer's
# own isolated logic (already covered by render_test.py).

import re
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from prosoc.nca.utils.papers import render

REPO_ROOT = Path(__file__).resolve().parents[4]
LUA_FILTER = REPO_ROOT / "papers" / "01_charter" / "strip_heading_numbers.lua"

# (pandoc source key, source path relative to REPO_ROOT) for every card
# actually included in the charter supplement, per papers/01_charter/sources.txt.
SOURCES = {
    "CHARTER": "src/prosoc/prnc/charter/charter.md",
    "FRONTAL_APPROACH": "src/prosoc/prnc/scenarios/frontal_approach/scenario.md",
    "SINGLE_FILE_HALLWAY": "src/prosoc/prnc/scenarios/single_file_hallway/scenario.md",
    "MOVABLE_OBSTRUCTION": "src/prosoc/prnc/scenarios/movable_obstruction/scenario.md",
    "NAVIGATE_POINT_TO_POINT": "src/prosoc/prnc/tasks/navigate_point_to_point/task.md",
    "DELIVER_OBJECT": "src/prosoc/prnc/tasks/deliver_object/task.md",
    "ROUTINE_DELIVERY": "src/prosoc/prnc/contexts/routine_delivery/context.md",
    "GUIDANCE_DOCENT": "src/prosoc/prnc/contexts/guidance_docent/context.md",
    "HIGH_URGENCY": "src/prosoc/prnc/contexts/high_urgency/context.md",
}

_FENCED_YAML_RE = re.compile(r"```yaml\n(.*?)```", re.DOTALL)
_LSTLISTING_RE = re.compile(
    r"\\begin\{lstlisting\}.*?\n(.*?)\\end\{lstlisting\}", re.DOTALL
)


def _render_real_source(key: str, relative_path: str) -> str:
    """Render one real charter-paper source card via real pandoc and
    return the rendered LaTeX fragment text."""
    with tempfile.TemporaryDirectory() as td:
        fragments_dir = Path(td)
        output = render.render_fragment(
            key,
            REPO_ROOT / relative_path,
            repo_root=REPO_ROOT,
            fragments_dir=fragments_dir,
            lua_filter=LUA_FILTER if key == "CHARTER" else None,
            log=None,
        )
        return output.read_text(encoding="utf-8")


def _extract_fenced_yaml(markdown_text: str) -> str:
    match = _FENCED_YAML_RE.search(markdown_text)
    if match is None:
        raise AssertionError("no fenced ```yaml block found in source")
    return match.group(1)


def _extract_lstlisting(fragment_text: str) -> str:
    match = _LSTLISTING_RE.search(fragment_text)
    if match is None:
        raise AssertionError("no \\begin{lstlisting} block found in rendered fragment")
    return match.group(1)


class TestYamlSemanticRoundTrip(unittest.TestCase):
    """Every source card's fenced YAML must parse to the same structure
    once it comes back out through pandoc's listings rendering -- not
    necessarily byte-identical (pandoc may trim trailing blank lines),
    but semantically equal."""

    def setUp(self):
        if shutil.which("pandoc") is None:
            self.skipTest("pandoc is not installed")

    def test_every_source_yaml_round_trips(self):
        for key, relative_path in SOURCES.items():
            with self.subTest(key=key):
                source_text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
                source_yaml = _extract_fenced_yaml(source_text)

                fragment_text = _render_real_source(key, relative_path)
                rendered_yaml = _extract_lstlisting(fragment_text)

                parsed_source = yaml.safe_load(source_yaml)
                parsed_rendered = yaml.safe_load(rendered_yaml)
                self.assertEqual(
                    parsed_source,
                    parsed_rendered,
                    f"{key}: rendered YAML listing doesn't match source structure",
                )


# (context source key, [(backtick-quoted identifier, ...), ...]) for every
# Context ID / Applies To Tasks value in the 3 context cards actually
# included in the paper.
_CONTEXT_IDENTIFIERS = {
    "ROUTINE_DELIVERY": ["service.routine_delivery", "deliver.object"],
    "GUIDANCE_DOCENT": ["guidance.docent", "navigate.lead_agent"],
    "HIGH_URGENCY": ["emergency.high_urgency", "*"],
}


class TestIdentifierSurvival(unittest.TestCase):
    """Context ID / Applies To Tasks identifiers (code spans in the
    source prose) must survive into the rendered LaTeX as \\texttt{...},
    with LaTeX's mandatory underscore-escaping normalized away before
    comparing -- a literal substring search would wrongly fail on
    'service.routine_delivery' vs. the escaped 'service.routine\\_delivery'
    pandoc must emit outside a verbatim-like environment."""

    def setUp(self):
        if shutil.which("pandoc") is None:
            self.skipTest("pandoc is not installed")

    def test_context_identifiers_survive_as_texttt(self):
        for key, identifiers in _CONTEXT_IDENTIFIERS.items():
            relative_path = SOURCES[key]
            fragment_text = _render_real_source(key, relative_path)
            # Normalize away LaTeX's mandatory underscore-escaping and any
            # line-wrap-inserted whitespace before searching.
            normalized = fragment_text.replace("\\_", "_")
            normalized = re.sub(r"\s+", " ", normalized)
            for identifier in identifiers:
                with self.subTest(key=key, identifier=identifier):
                    expected = f"\\texttt{{{identifier}}}"
                    self.assertIn(
                        expected,
                        normalized,
                        f"{key}: identifier {identifier!r} not recoverable as "
                        f"\\texttt{{...}} in the rendered fragment",
                    )


if __name__ == "__main__":
    unittest.main()
