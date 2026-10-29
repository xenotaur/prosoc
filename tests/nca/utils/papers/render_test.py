import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

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


class TestToolVersionParsing(unittest.TestCase):

    def test_parses_leading_version_token(self):
        self.assertEqual(render.parse_tool_version("3.10.1", tool="pandoc"), "3.10.1")

    def test_rejects_empty_output(self):
        with self.assertRaisesRegex(ValueError, "could not parse"):
            render.parse_tool_version("", tool="pandoc")


class TestPandocVersionCheck(unittest.TestCase):

    def test_accepts_matching_pinned_version(self):
        def fake_runner(args, **kwargs):
            return SimpleNamespace(stdout=f"pandoc {render.PANDOC_PINNED_VERSION}\n")

        version = render.check_pandoc_version(runner=fake_runner)

        self.assertEqual(version, render.PANDOC_PINNED_VERSION)

    def test_rejects_mismatched_version(self):
        def fake_runner(args, **kwargs):
            return SimpleNamespace(stdout="pandoc 2.9.2\n")

        with self.assertRaisesRegex(ValueError, "version mismatch"):
            render.check_pandoc_version(runner=fake_runner)

    def test_wraps_failed_invocation_with_clear_message(self):
        def failing_runner(args, **kwargs):
            raise subprocess.CalledProcessError(1, args)

        with self.assertRaisesRegex(RuntimeError, "pandoc --version failed"):
            render.check_pandoc_version(runner=failing_runner)


class TestTexEngineVersion(unittest.TestCase):

    def test_returns_first_line_of_version_output(self):
        def fake_runner(args, **kwargs):
            return SimpleNamespace(
                stdout="pdfTeX 3.141592653-2.6-1.40.24 (TeX Live 2022)\nkpathsea ...\n"
            )

        version = render.get_tex_engine_version(runner=fake_runner)

        self.assertEqual(version, "pdfTeX 3.141592653-2.6-1.40.24 (TeX Live 2022)")

    def test_wraps_failed_invocation_with_clear_message(self):
        def failing_runner(args, **kwargs):
            raise subprocess.CalledProcessError(1, args)

        with self.assertRaisesRegex(RuntimeError, "pdflatex --version failed"):
            render.get_tex_engine_version(runner=failing_runner)


class TestRequireTool(unittest.TestCase):

    def test_returns_path_when_found(self):
        path = render.require_tool("pandoc", which=lambda name: "/usr/bin/pandoc")

        self.assertEqual(path, "/usr/bin/pandoc")

    def test_raises_clearly_when_missing(self):
        with self.assertRaisesRegex(FileNotFoundError, "not installed or not on PATH"):
            render.require_tool("pdflatex", which=lambda name: None)


class TestClassFileCheck(unittest.TestCase):

    def test_passes_when_kpsewhich_resolves_class(self):
        def fake_runner(args, **kwargs):
            return SimpleNamespace(stdout="/usr/texmf/frontiers_suppmat.cls\n")

        with mock.patch.object(shutil, "which", return_value="/usr/bin/kpsewhich"):
            render.check_class_file("frontiers_suppmat", runner=fake_runner)

    def test_raises_clearly_when_class_not_found(self):
        def fake_runner(args, **kwargs):
            return SimpleNamespace(stdout="")

        with mock.patch.object(shutil, "which", return_value="/usr/bin/kpsewhich"):
            with self.assertRaisesRegex(FileNotFoundError, "not committed to the repo"):
                render.check_class_file("frontiers_suppmat", runner=fake_runner)

    def test_raises_clearly_when_kpsewhich_itself_missing(self):
        with mock.patch.object(shutil, "which", return_value=None):
            with self.assertRaisesRegex(FileNotFoundError, "kpsewhich"):
                render.check_class_file(
                    "frontiers_suppmat", runner=lambda *a, **k: None
                )


class TestSemanticChecks(unittest.TestCase):

    def test_runs_configured_modules_against_repo_root(self):
        calls = []

        def fake_runner(args, **kwargs):
            calls.append((args, kwargs))
            return SimpleNamespace(returncode=0)

        render.run_semantic_checks(Path("/repo"), runner=fake_runner, log=None)

        self.assertEqual(calls[0][0][0], sys.executable)
        self.assertEqual(calls[0][0][1], "-m")
        self.assertEqual(calls[0][0][2], "unittest")
        self.assertEqual(tuple(calls[0][0][3:]), render.SEMANTIC_CHECK_MODULES)
        self.assertEqual(calls[0][1]["cwd"], Path("/repo"))

    def test_wraps_failure_with_clear_message(self):
        def failing_runner(args, **kwargs):
            raise subprocess.CalledProcessError(1, args)

        with self.assertRaisesRegex(RuntimeError, "semantic/LaTeX regression"):
            render.run_semantic_checks(Path("/repo"), runner=failing_runner, log=None)


class TestCompilePdf(unittest.TestCase):

    def test_returns_pdf_path_on_success(self):
        calls = []

        def fake_runner(args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=0)

        with tempfile.TemporaryDirectory() as td:
            build_dir = Path(td)
            tex_file = build_dir / "rendered.tex"
            tex_file.write_text("\\documentclass{article}\n", encoding="utf-8")

            pdf_path = render.compile_pdf(
                tex_file, build_dir, runner=fake_runner, log=None
            )

            self.assertEqual(pdf_path, build_dir / "rendered.pdf")
            self.assertIn("-halt-on-error", calls[0])
            self.assertIn("-interaction=nonstopmode", calls[0])

    def test_wraps_pdflatex_failure_with_log_path(self):
        def failing_runner(args, **kwargs):
            raise subprocess.CalledProcessError(1, args)

        with tempfile.TemporaryDirectory() as td:
            build_dir = Path(td)
            tex_file = build_dir / "rendered.tex"

            with self.assertRaisesRegex(RuntimeError, "rendered.log"):
                render.compile_pdf(tex_file, build_dir, runner=failing_runner, log=None)


class TestExtractPdfText(unittest.TestCase):

    def test_runs_pdftotext_with_layout(self):
        calls = []

        def fake_runner(args, **kwargs):
            calls.append(args)
            return SimpleNamespace(stdout="extracted text")

        text = render.extract_pdf_text(Path("out.pdf"), runner=fake_runner)

        self.assertEqual(text, "extracted text")
        self.assertIn("-layout", calls[0])


class TestPdfPageCount(unittest.TestCase):

    def test_counts_form_feeds_plus_one(self):
        self.assertEqual(
            render.count_pdf_pages("page one\x0cpage two\x0cpage three"), 3
        )

    def test_single_page_has_no_form_feed(self):
        self.assertEqual(render.count_pdf_pages("only page"), 1)

    def test_empty_text_is_zero_pages(self):
        self.assertEqual(render.count_pdf_pages(""), 0)


class TestPdfTextRegressions(unittest.TestCase):

    def test_detects_known_corruption(self):
        corrupted = "...the robot itselfby moving around the obstructionthereby..."

        findings = render.check_pdf_text_regressions(corrupted)

        self.assertIn("itselfby", findings)
        self.assertIn("obstructionthereby", findings)

    def test_clean_text_has_no_findings(self):
        self.assertEqual(render.check_pdf_text_regressions("clean prose"), [])


class TestBuildPdf(unittest.TestCase):
    """Orchestration tests with every external tool faked -- real tool
    availability (pdflatex/kpsewhich) is irrelevant here; only the pipeline
    sequencing and failure propagation are under test."""

    def _fake_runner(self, *, pdf_text="clean extracted text"):
        def runner(args, **kwargs):
            exe = Path(args[0]).name
            if exe == "pandoc":
                return SimpleNamespace(
                    stdout=f"pandoc {render.PANDOC_PINNED_VERSION}\n"
                )
            if exe == "kpsewhich":
                return SimpleNamespace(stdout="/texmf/frontiers_suppmat.cls\n")
            if exe == "pdflatex" and "--version" in args:
                return SimpleNamespace(stdout="pdfTeX 3.14\n")
            if exe == "pdflatex":
                return SimpleNamespace(returncode=0)
            if exe == "pdftotext":
                return SimpleNamespace(stdout=pdf_text)
            raise AssertionError(f"unexpected command: {args}")

        return runner

    def _write_fixture_paper(self, root: Path) -> tuple[Path, Path]:
        paper_dir = root / "papers" / "01_charter"
        paper_dir.mkdir(parents=True)
        build_dir = root / "build" / "papers" / "01_charter"
        source = root / "charter.md"
        source.write_text("# Charter\n", encoding="utf-8")
        (paper_dir / "sources.txt").write_text(
            f"CHARTER {source.relative_to(root)}\n", encoding="utf-8"
        )
        (paper_dir / "template.tex").write_text("@@CHARTER@@\n", encoding="utf-8")
        return paper_dir, build_dir

    def test_full_pipeline_reports_versions_path_and_page_count(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper_dir, build_dir = self._write_fixture_paper(root)

            with (
                mock.patch.object(shutil, "which", return_value="/usr/bin/tool"),
                mock.patch.object(render, "require_tool", return_value="/usr/bin/tool"),
            ):
                report = render.build_pdf(
                    repo_root=root,
                    paper_dir=paper_dir,
                    build_dir=build_dir,
                    runner=self._fake_runner(pdf_text="one\x0ctwo"),
                    skip_semantic_checks=True,
                    log=None,
                )

            self.assertEqual(report["pandoc_version"], render.PANDOC_PINNED_VERSION)
            self.assertEqual(report["tex_engine_version"], "pdfTeX 3.14")
            self.assertEqual(report["pdf_path"], build_dir / "rendered.pdf")
            self.assertEqual(report["page_count"], 2)

    def test_stops_before_rendering_on_pandoc_version_mismatch(self):
        def fake_runner(args, **kwargs):
            if Path(args[0]).name == "pandoc":
                return SimpleNamespace(stdout="pandoc 2.9.2\n")
            raise AssertionError(f"should not reach: {args}")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper_dir, build_dir = self._write_fixture_paper(root)

            with mock.patch.object(shutil, "which", return_value="/usr/bin/tool"):
                with self.assertRaisesRegex(ValueError, "version mismatch"):
                    render.build_pdf(
                        repo_root=root,
                        paper_dir=paper_dir,
                        build_dir=build_dir,
                        runner=fake_runner,
                        skip_semantic_checks=True,
                        log=None,
                    )

    def test_raises_on_pdf_text_regression(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper_dir, build_dir = self._write_fixture_paper(root)

            with (
                mock.patch.object(shutil, "which", return_value="/usr/bin/tool"),
                mock.patch.object(render, "require_tool", return_value="/usr/bin/tool"),
            ):
                with self.assertRaisesRegex(RuntimeError, "PDF-text regression"):
                    render.build_pdf(
                        repo_root=root,
                        paper_dir=paper_dir,
                        build_dir=build_dir,
                        runner=self._fake_runner(pdf_text="broke itselfby here"),
                        skip_semantic_checks=True,
                        log=None,
                    )


class TestMainPdfFlag(unittest.TestCase):

    def test_pdf_flag_invokes_build_pdf_and_prints_report(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper_dir = root / "papers" / "01_charter"
            paper_dir.mkdir(parents=True)
            build_dir = root / "build"
            pdf_path = build_dir / "rendered.pdf"

            with mock.patch.object(
                render,
                "build_pdf",
                return_value={
                    "pandoc_version": "3.10.1",
                    "tex_engine_version": "pdfTeX 3.14",
                    "pdf_path": pdf_path,
                    "page_count": 7,
                },
            ) as fake_build_pdf:
                result = render.main(
                    repo_root=root,
                    paper_dir=paper_dir,
                    build_dir=build_dir,
                    argv=["--pdf"],
                )

            self.assertEqual(result, 0)
            fake_build_pdf.assert_called_once_with(
                repo_root=root, paper_dir=paper_dir, build_dir=build_dir
            )

    def test_pdf_flag_reports_clear_error_on_missing_tool(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper_dir = root / "papers" / "01_charter"
            paper_dir.mkdir(parents=True)
            build_dir = root / "build"

            with mock.patch.object(
                render,
                "build_pdf",
                side_effect=FileNotFoundError(
                    "pdflatex is not installed or not on PATH"
                ),
            ):
                result = render.main(
                    repo_root=root,
                    paper_dir=paper_dir,
                    build_dir=build_dir,
                    argv=["--pdf"],
                )

            self.assertEqual(result, 1)

    def test_no_pdf_flag_keeps_tex_only_behavior(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper_dir = root / "papers" / "01_charter"
            paper_dir.mkdir(parents=True)
            build_dir = root / "build"

            with mock.patch.object(render, "build_pdf") as fake_build_pdf:
                with mock.patch.object(
                    render, "render_paper", return_value=build_dir / "rendered.tex"
                ) as fake_render_paper:
                    result = render.main(
                        repo_root=root,
                        paper_dir=paper_dir,
                        build_dir=build_dir,
                        argv=[],
                    )

            self.assertEqual(result, 0)
            fake_render_paper.assert_called_once()
            fake_build_pdf.assert_not_called()


class TestPdfBuildRealEnvironment(unittest.TestCase):
    """Exercises --pdf's fail-fast behavior against this machine's real
    tools, without requiring pdflatex or the (uncommitted) Frontiers class
    file to be present -- the acceptance criterion is a clear failure, which
    this sandbox's actual missing-pdflatex state demonstrates directly."""

    def test_pdf_flag_fails_clearly_when_pdflatex_missing(self):
        if shutil.which("pdflatex") is not None:
            self.skipTest("pdflatex is installed; missing-tool path not exercised")
        if shutil.which("pandoc") is None:
            self.skipTest("pandoc is not installed")

        REPO_ROOT_LOCAL = REPO_ROOT
        paper_dir = REPO_ROOT_LOCAL / "papers" / "01_charter"
        with tempfile.TemporaryDirectory() as td:
            build_dir = Path(td)

            result = render.main(
                repo_root=REPO_ROOT_LOCAL,
                paper_dir=paper_dir,
                build_dir=build_dir,
                argv=["--pdf"],
            )

        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
