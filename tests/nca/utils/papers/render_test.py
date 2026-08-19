import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from prosoc.nca.utils.papers import render


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


if __name__ == "__main__":
    unittest.main()
