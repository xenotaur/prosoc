import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from prosoc.nca.utils.papers import render

REPO_ROOT = Path(__file__).resolve().parents[4]
LUA_FILTER = REPO_ROOT / "papers" / "01_charter" / "strip_heading_numbers.lua"


class TestFragmentFixups(unittest.TestCase):

    def test_applies_listing_style_to_plain_listing(self):
        fragment = "\\begin{lstlisting}\nid: P0\n\\end{lstlisting}\n"

        fixed = render.apply_fragment_fixups(fragment)

        self.assertIn("\\begin{lstlisting}[style=literatecard]", fixed)
        self.assertNotIn("\\begin{lstlisting}\n", fixed)

    def test_applies_listing_style_to_listing_with_existing_options(self):
        fragment = "\\begin{lstlisting}[language=yaml]\nid: P0\n\\end{lstlisting}\n"

        fixed = render.apply_fragment_fixups(fragment)

        self.assertIn("\\begin{lstlisting}[style=literatecard]", fixed)
        self.assertNotIn("language=yaml", fixed)

    def test_removes_pandoc_horizontal_rule(self):
        fragment = f"before\n\n{render.PANDOC_HORIZONTAL_RULE}\n\nafter\n"

        fixed = render.apply_fragment_fixups(fragment)

        self.assertEqual(fixed, "before\n\nafter\n")

    def test_converts_passthrough_lstinline_to_texttt(self):
        fragment = r"See \passthrough{\lstinline!foo_bar!}."

        fixed = render.apply_fragment_fixups(fragment)

        self.assertEqual(fixed, r"See \texttt{foo_bar}.")


class TestSources(unittest.TestCase):

    def test_loads_sources_and_ignores_comments(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "prosoc" / "charter" / "charter.md"
            source.parent.mkdir(parents=True)
            source.write_text("# Charter\n", encoding="utf-8")
            sources_file = root / "sources.txt"
            sources_file.write_text(
                "# comment\n\nCHARTER prosoc/charter/charter.md\n",
                encoding="utf-8",
            )

            sources = render.load_sources(sources_file, root)

            self.assertEqual(sources, [("CHARTER", source)])

    def test_rejects_malformed_source_line(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sources_file = root / "sources.txt"
            sources_file.write_text("CHARTER\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "expected 'KEY path'"):
                render.load_sources(sources_file, root)

    def test_rejects_missing_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sources_file = root / "sources.txt"
            sources_file.write_text(
                "CHARTER prosoc/charter/charter.md\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(FileNotFoundError, "source does not exist"):
                render.load_sources(sources_file, root)

    def test_rejects_invalid_source_key(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source.md"
            source.write_text("# Source\n", encoding="utf-8")
            sources_file = root / "sources.txt"
            sources_file.write_text("BAD-KEY source.md\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "invalid source key"):
                render.load_sources(sources_file, root)

    def test_rejects_absolute_source_path(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source.md"
            source.write_text("# Source\n", encoding="utf-8")
            sources_file = root / "sources.txt"
            sources_file.write_text(f"CHARTER {source}\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "source path must stay"):
                render.load_sources(sources_file, root)

    def test_rejects_parent_traversal_source_path(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            outside = root.parent / "outside.md"
            outside.write_text("# Outside\n", encoding="utf-8")
            sources_file = root / "sources.txt"
            sources_file.write_text("CHARTER ../outside.md\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "source path must stay"):
                render.load_sources(sources_file, root)

    def test_rejects_symlink_source_path_that_escapes_repo_root(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            outside = root.parent / "outside.md"
            outside.write_text("# Outside\n", encoding="utf-8")
            link = root / "linked.md"
            try:
                link.symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"symlinks unavailable: {exc}")

            sources_file = root / "sources.txt"
            sources_file.write_text("CHARTER linked.md\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "escapes repository root"):
                render.load_sources(sources_file, root)


class TestPandocArgs(unittest.TestCase):

    def test_charter_keeps_heading_level(self):
        source = Path("prosoc/charter/charter.md")

        args = render.build_pandoc_args("CHARTER", source)

        self.assertNotIn("--shift-heading-level-by=1", args)
        self.assertEqual(args[-1], str(source))

    def test_non_charter_shifts_heading_level(self):
        source = Path("prosoc/scenarios/frontal_approach/scenario.md")

        args = render.build_pandoc_args("FRONTAL_APPROACH", source)

        self.assertIn("--shift-heading-level-by=1", args)
        self.assertEqual(args[-1], str(source))

    def test_rejects_invalid_key_before_building_args(self):
        with self.assertRaisesRegex(ValueError, "invalid source key"):
            render.build_pandoc_args("../BAD", Path("source.md"))

    def test_charter_adds_lua_filter_when_given(self):
        source = Path("prosoc/charter/charter.md")
        lua_filter = Path("papers/01_charter/strip_heading_numbers.lua")

        args = render.build_pandoc_args("CHARTER", source, lua_filter=lua_filter)

        self.assertIn(f"--lua-filter={lua_filter}", args)
        self.assertNotIn("--shift-heading-level-by=1", args)

    def test_charter_omits_lua_filter_when_not_given(self):
        source = Path("prosoc/charter/charter.md")

        args = render.build_pandoc_args("CHARTER", source)

        self.assertFalse(any(a.startswith("--lua-filter=") for a in args))

    def test_non_charter_never_gets_lua_filter_even_if_given(self):
        source = Path("prosoc/scenarios/frontal_approach/scenario.md")
        lua_filter = Path("papers/01_charter/strip_heading_numbers.lua")

        args = render.build_pandoc_args(
            "FRONTAL_APPROACH", source, lua_filter=lua_filter
        )

        self.assertFalse(any(a.startswith("--lua-filter=") for a in args))
        self.assertIn("--shift-heading-level-by=1", args)


class TestTemplateSubstitution(unittest.TestCase):

    def test_replaces_single_placeholder(self):
        rendered = render.replace_placeholder(
            "before\n@@CHARTER@@\nafter\n",
            template_file=Path("template.tex"),
            key="CHARTER",
            fragment="fragment",
        )

        self.assertEqual(rendered, "before\nfragment\nafter\n")

    def test_rejects_missing_placeholder(self):
        with self.assertRaisesRegex(ValueError, "expected exactly one @@CHARTER@@"):
            render.replace_placeholder(
                "no placeholder",
                template_file=Path("template.tex"),
                key="CHARTER",
                fragment="fragment",
            )

    def test_rejects_duplicate_placeholder(self):
        with self.assertRaisesRegex(ValueError, "found 2"):
            render.replace_placeholder(
                "@@CHARTER@@\n@@CHARTER@@\n",
                template_file=Path("template.tex"),
                key="CHARTER",
                fragment="fragment",
            )

    def test_rejects_unresolved_placeholders(self):
        with self.assertRaisesRegex(ValueError, "Unresolved placeholders"):
            render.check_unresolved_placeholders("@@MISSING@@")


class TestLuaFilterIntegration(unittest.TestCase):
    """Runs the real pandoc + strip_heading_numbers.lua, not a fake runner --
    covers what the fake-runner unit tests above can't: that the filter file
    actually parses as Lua and does the right thing to real pandoc output."""

    def setUp(self):
        if shutil.which("pandoc") is None:
            self.skipTest("pandoc is not installed")
        if not LUA_FILTER.is_file():
            self.skipTest(f"lua filter not found at {LUA_FILTER}")

    def test_strips_authored_number_from_numbered_heading(self):
        result = subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "latex", f"--lua-filter={LUA_FILTER}"],
            input="## 1. Purpose of This Charter\n",
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )

        self.assertIn("\\subsection{Purpose of This Charter}", result.stdout)
        self.assertNotIn("1. Purpose", result.stdout)

    def test_leaves_unnumbered_heading_unchanged(self):
        result = subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "latex", f"--lua-filter={LUA_FILTER}"],
            input="### Normative Statement\n",
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )

        self.assertIn("\\subsubsection{Normative Statement}", result.stdout)

    def test_leaves_dotted_sub_number_unchanged(self):
        # Only a bare "N." token followed by a space is stripped -- a
        # dotted sub-number like "4.1" is a single token ("4.1", no
        # trailing-only period) and must not be touched.
        result = subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "latex", f"--lua-filter={LUA_FILTER}"],
            input="## 4.1 Sub-numbered Heading\n",
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )

        self.assertIn("4.1 Sub-numbered Heading", result.stdout)


# (pandoc source key, source path relative to REPO_ROOT, label substrings
# expected to introduce a Markdown list in the real source) -- every card
# actually affected by the collapsed-list defect found in the 2026-10-26
# charter supplement pipeline audit.
_LIST_COLLAPSE_CASES = [
    (
        "NAVIGATE_POINT_TO_POINT",
        "src/prosoc/prnc/tasks/navigate_point_to_point/task.md",
        ["Includes:", "Excludes:"],
    ),
    (
        "DELIVER_OBJECT",
        "src/prosoc/prnc/tasks/deliver_object/task.md",
        ["Includes:", "Excludes:", "It frequently interacts with:"],
    ),
    (
        "ROUTINE_DELIVERY",
        "src/prosoc/prnc/contexts/routine_delivery/context.md",
        [
            "Includes:",
            "Excludes:",
            "Key normative expectations include:",
            "Geometric Factors",
            "Operational Factors",
            "Common tensions include:",
        ],
    ),
    (
        "GUIDANCE_DOCENT",
        "src/prosoc/prnc/contexts/guidance_docent/context.md",
        [
            "Includes:",
            "Excludes:",
            "Key normative expectations include:",
            "Geometric Factors",
            "Operational Factors",
            "Common tensions include:",
        ],
    ),
    (
        "HIGH_URGENCY",
        "src/prosoc/prnc/contexts/high_urgency/context.md",
        [
            "Includes:",
            "Excludes:",
            "Key normative expectations include:",
            "Geometric Factors",
            "Operational Factors",
            "Common tensions include:",
        ],
    ),
]


class TestListCollapseRegression(unittest.TestCase):
    """Regression coverage for the collapsed-list defect found in the
    2026-10-26 charter supplement pipeline audit: a bold or plain label
    immediately followed by a Markdown list, with no blank line between
    them, rendered as run-on prose ("Includes: - item one - item two")
    instead of a proper LaTeX list -- fixed at the source level by
    WI-CHARTER-SUPPLEMENT-SOURCE-FIXES. Runs real pandoc against the real
    source cards, since the defect was in the source text, not in this
    module's own fixup logic."""

    def setUp(self):
        if shutil.which("pandoc") is None:
            self.skipTest("pandoc is not installed")

    def test_no_collapsed_list_after_known_labels(self):
        for key, relative_path, labels in _LIST_COLLAPSE_CASES:
            with tempfile.TemporaryDirectory() as td:
                fragments_dir = Path(td)
                output = render.render_fragment(
                    key,
                    REPO_ROOT / relative_path,
                    repo_root=REPO_ROOT,
                    fragments_dir=fragments_dir,
                    log=None,
                )
                text = output.read_text(encoding="utf-8")

            for label in labels:
                with self.subTest(key=key, label=label):
                    idx = text.find(label)
                    self.assertNotEqual(idx, -1, f"{key}: label {label!r} not found")
                    after = text[idx + len(label) :]
                    match = re.search(r"\\begin\{itemize\}", after)
                    self.assertIsNotNone(
                        match, f"{key}: no itemize list follows {label!r}"
                    )
                    between = after[: match.start()].strip()
                    # A bolded label (e.g. "\textbf{Includes:}") leaves one
                    # closing brace in `between`; strip it before asserting
                    # nothing else (i.e. no collapsed run-on text) remains.
                    if between.startswith("}"):
                        between = between[1:].strip()
                    self.assertEqual(
                        between,
                        "",
                        f"{key}: {label!r} not immediately followed by a clean "
                        f"list (found collapsed run-on text: {between!r})",
                    )


class TestHeadingNumberRegression(unittest.TestCase):
    """Regression coverage for the double-numbered-heading defect: every
    heading in the real charter.md must render with no authored
    heading-number prefix, checked across the whole document rather than
    a few synthetic examples (TestLuaFilterIntegration covers the filter's
    own logic in isolation)."""

    def setUp(self):
        if shutil.which("pandoc") is None:
            self.skipTest("pandoc is not installed")
        if not LUA_FILTER.is_file():
            self.skipTest(f"lua filter not found at {LUA_FILTER}")

    def test_no_charter_heading_keeps_authored_number(self):
        with tempfile.TemporaryDirectory() as td:
            fragments_dir = Path(td)
            output = render.render_fragment(
                "CHARTER",
                REPO_ROOT / "src/prosoc/prnc/charter/charter.md",
                repo_root=REPO_ROOT,
                fragments_dir=fragments_dir,
                lua_filter=LUA_FILTER,
                log=None,
            )
            text = output.read_text(encoding="utf-8")

        headings = re.findall(r"\\subsection\{([^}]*)\}", text)
        self.assertGreater(len(headings), 0, "no \\subsection{...} headings found")
        for heading in headings:
            with self.subTest(heading=heading):
                self.assertNotRegex(
                    heading,
                    r"^\d+\.\s",
                    f"heading {heading!r} still carries an authored number prefix",
                )


class TestRendering(unittest.TestCase):

    def test_render_fragment_uses_fake_runner_and_writes_fixed_fragment(self):
        calls = []

        def fake_runner(*args, **kwargs):
            calls.append((args, kwargs))
            return SimpleNamespace(
                stdout="\\begin{lstlisting}\nid: P0\n\\end{lstlisting}\n"
            )

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source.md"
            source.write_text("# Source\n", encoding="utf-8")
            fragments_dir = root / "build" / "fragments"
            fragments_dir.mkdir(parents=True)

            output = render.render_fragment(
                "CHARTER",
                source,
                repo_root=root,
                fragments_dir=fragments_dir,
                runner=fake_runner,
                log=None,
            )

            self.assertEqual(output, fragments_dir / "charter.tex")
            self.assertIn(
                "\\begin{lstlisting}[style=literatecard]",
                output.read_text(encoding="utf-8"),
            )
            self.assertEqual(calls[0][0][0][-1], str(source))
            self.assertIs(calls[0][1]["stdin"], subprocess.DEVNULL)
            self.assertIs(calls[0][1]["stdout"], subprocess.PIPE)
            self.assertTrue(calls[0][1]["check"])
            self.assertTrue(calls[0][1]["text"])

    def test_render_paper_assembles_template_with_fake_runner(self):
        def fake_runner(args, **kwargs):
            key = Path(args[-1]).stem.upper()
            return SimpleNamespace(stdout=f"fragment {key}\n")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper_dir = root / "papers" / "01_charter"
            paper_dir.mkdir(parents=True)
            build_dir = root / "build" / "papers" / "01_charter"

            charter = root / "charter.md"
            card = root / "card.md"
            charter.write_text("# Charter\n", encoding="utf-8")
            card.write_text("# Card\n", encoding="utf-8")
            (paper_dir / "sources.txt").write_text(
                f"CHARTER {charter.relative_to(root)}\n"
                f"CARD {card.relative_to(root)}\n",
                encoding="utf-8",
            )
            (paper_dir / "template.tex").write_text(
                "A\n@@CHARTER@@\nB\n@@CARD@@\n",
                encoding="utf-8",
            )

            output = render.render_paper(
                repo_root=root,
                paper_dir=paper_dir,
                build_dir=build_dir,
                runner=fake_runner,
                require_pandoc=False,
                log=None,
            )

            self.assertEqual(output, build_dir / "rendered.tex")
            self.assertEqual(
                output.read_text(encoding="utf-8"),
                "A\nfragment CHARTER\n\nB\nfragment CARD\n\n",
            )

    def test_render_paper_passes_lua_filter_only_for_charter_when_present(self):
        calls = {}

        def fake_runner(args, **kwargs):
            key = Path(args[-1]).stem.upper()
            calls[key] = args
            return SimpleNamespace(stdout=f"fragment {key}\n")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper_dir = root / "papers" / "01_charter"
            paper_dir.mkdir(parents=True)
            build_dir = root / "build" / "papers" / "01_charter"

            charter = root / "charter.md"
            card = root / "card.md"
            charter.write_text("# Charter\n", encoding="utf-8")
            card.write_text("# Card\n", encoding="utf-8")
            (paper_dir / "sources.txt").write_text(
                f"CHARTER {charter.relative_to(root)}\n"
                f"CARD {card.relative_to(root)}\n",
                encoding="utf-8",
            )
            (paper_dir / "template.tex").write_text(
                "A\n@@CHARTER@@\nB\n@@CARD@@\n",
                encoding="utf-8",
            )
            lua_filter = paper_dir / "strip_heading_numbers.lua"
            lua_filter.write_text("-- test stub\n", encoding="utf-8")

            render.render_paper(
                repo_root=root,
                paper_dir=paper_dir,
                build_dir=build_dir,
                runner=fake_runner,
                require_pandoc=False,
                log=None,
            )

            self.assertIn(f"--lua-filter={lua_filter}", calls["CHARTER"])
            self.assertFalse(any(a.startswith("--lua-filter=") for a in calls["CARD"]))

    def test_render_paper_omits_lua_filter_when_file_absent(self):
        def fake_runner(args, **kwargs):
            key = Path(args[-1]).stem.upper()
            return SimpleNamespace(stdout=f"fragment {key}\n")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper_dir = root / "papers" / "01_charter"
            paper_dir.mkdir(parents=True)
            build_dir = root / "build" / "papers" / "01_charter"

            charter = root / "charter.md"
            charter.write_text("# Charter\n", encoding="utf-8")
            (paper_dir / "sources.txt").write_text(
                f"CHARTER {charter.relative_to(root)}\n",
                encoding="utf-8",
            )
            (paper_dir / "template.tex").write_text("@@CHARTER@@\n", encoding="utf-8")
            # No strip_heading_numbers.lua written -- must not raise or add
            # a --lua-filter flag pointing at a nonexistent file.

            output = render.render_paper(
                repo_root=root,
                paper_dir=paper_dir,
                build_dir=build_dir,
                runner=fake_runner,
                require_pandoc=False,
                log=None,
            )

            self.assertEqual(output.read_text(encoding="utf-8"), "fragment CHARTER\n\n")


if __name__ == "__main__":
    unittest.main()
