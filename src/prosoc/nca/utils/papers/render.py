"""Render paper supplements from Markdown card sources."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

PANDOC_HORIZONTAL_RULE = "\\begin{center}\\rule{0.5\\linewidth}{0.5pt}\\end{center}"
SOURCE_KEY_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")

# The pipeline's reproducibility depends on an unpinned Pandoc version; the
# 2026-10-26 charter supplement audit observed 3.10.1 and 2.9.2 across two
# sandboxes, straddling the --listings-spelling deprecation above. Pin an
# exact expected version and fail fast on drift rather than silently
# rendering with whatever happens to be on PATH.
PANDOC_PINNED_VERSION = "3.10.1"

# The Frontiers supplement's LaTeX class; not committed to this repository
# (publisher asset, licensing unconfirmed -- see
# WI-CHARTER-SUPPLEMENT-PDF-BUILD's Risk Notes). --pdf must fail clearly,
# not with a wall of pdflatex log output, when it isn't supplied locally.
FRONTIERS_TEX_CLASS = "frontiers_suppmat"

# Default semantic/LaTeX regression suite to run before compiling a PDF
# (WI-CHARTER-SUPPLEMENT-TEST-COVERAGE's tests).
SEMANTIC_CHECK_MODULES = (
    "tests.nca.utils.papers.render_test",
    "tests.nca.utils.papers.paper_semantics_test",
)

# Concrete corrupted substrings the 2026-10-26 audit reproduced from a live
# pdflatex+pdftotext round trip with default (non-outline) fonts -- en/em
# dashes silently dropped from ordinary prose and lstlisting content alike.
KNOWN_PDF_TEXT_CORRUPTIONS = ("P1P9", "itselfby", "obstructionthereby")

Runner = Callable[..., Any]


def apply_fragment_fixups(fragment: str) -> str:
    """Apply deterministic publication-specific LaTeX fragment fixups."""
    fragment = re.sub(
        r"\\begin\{lstlisting\}(?:\[[^\]]*\])?",
        r"\\begin{lstlisting}[style=literatecard]",
        fragment,
    )
    fragment = re.sub(
        rf"\n*{re.escape(PANDOC_HORIZONTAL_RULE)}\n*",
        "\n\n",
        fragment,
    )
    fragment = re.sub(
        r"\\passthrough\{\\lstinline!([^!]*)!\}",
        r"\\texttt{\1}",
        fragment,
    )
    return fragment


def load_sources(sources_file: Path, repo_root: Path) -> list[tuple[str, Path]]:
    """Load ``KEY path`` source entries from a paper sources manifest."""
    sources: list[tuple[str, Path]] = []
    resolved_repo_root = repo_root.resolve()

    for line_number, raw_line in enumerate(
        sources_file.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"{sources_file}:{line_number}: expected 'KEY path'")

        key, relative_path = parts
        if SOURCE_KEY_RE.fullmatch(key) is None:
            raise ValueError(f"{sources_file}:{line_number}: invalid source key: {key}")

        source_path = Path(relative_path)
        if source_path.is_absolute() or ".." in source_path.parts:
            raise ValueError(
                f"{sources_file}:{line_number}: source path must stay under "
                f"repository root: {relative_path}"
            )

        source = repo_root / source_path

        if not source.is_file():
            raise FileNotFoundError(
                f"{sources_file}:{line_number}: source does not exist: {source}"
            )

        try:
            source.resolve().relative_to(resolved_repo_root)
        except ValueError as exc:
            raise ValueError(
                f"{sources_file}:{line_number}: source path escapes repository "
                f"root: {relative_path}"
            ) from exc

        sources.append((key, source))

    return sources


def build_pandoc_args(
    key: str,
    source: Path,
    *,
    pandoc: str = "pandoc",
    lua_filter: Path | None = None,
) -> list[str]:
    """Build the Pandoc command for one source fragment."""
    if SOURCE_KEY_RE.fullmatch(key) is None:
        raise ValueError(f"invalid source key: {key}")

    pandoc_args = [
        pandoc,
        "-f",
        "markdown",
        "-t",
        "latex",
        # Pandoc 3.10 deprecates --listings in favor of this spelling.
        "--syntax-highlighting=idiomatic",
    ]

    # The charter is a top-level section in the supplement. All other normative
    # cards are inserted under hand-authored category sections, so shift their
    # Markdown heading hierarchy down by one.
    if key != "CHARTER":
        pandoc_args.append("--shift-heading-level-by=1")
    elif lua_filter is not None:
        # The charter's Markdown headings are hand-numbered (e.g. "## 1.
        # Purpose..."); the Frontiers class numbers them again at compile
        # time. Scoped to the charter only -- other cards' headings aren't
        # authored-numbered (see strip_heading_numbers.lua).
        pandoc_args.append(f"--lua-filter={lua_filter}")

    # Always append the source path. If Pandoc is invoked without an input file,
    # it reads stdin and can appear to hang.
    pandoc_args.append(str(source))
    return pandoc_args


def render_fragment(
    key: str,
    source: Path,
    *,
    repo_root: Path,
    fragments_dir: Path,
    runner: Runner = subprocess.run,
    pandoc: str = "pandoc",
    lua_filter: Path | None = None,
    log: Callable[[str], None] | None = print,
) -> Path:
    """Render one Markdown source to a fixed-up LaTeX fragment file."""
    if SOURCE_KEY_RE.fullmatch(key) is None:
        raise ValueError(f"invalid source key: {key}")

    output = fragments_dir / f"{key.lower()}.tex"

    if log is not None:
        log(
            f"Rendering {source.relative_to(repo_root)} -> "
            f"{output.relative_to(repo_root)}"
        )

    completed = runner(
        build_pandoc_args(key, source, pandoc=pandoc, lua_filter=lua_filter),
        cwd=repo_root,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        check=True,
        text=True,
    )
    output.write_text(apply_fragment_fixups(completed.stdout), encoding="utf-8")

    return output


def replace_placeholder(
    rendered: str,
    *,
    template_file: Path,
    key: str,
    fragment: str,
) -> str:
    """Replace exactly one template placeholder with a rendered fragment."""
    placeholder = f"@@{key}@@"
    count = rendered.count(placeholder)
    if count != 1:
        raise ValueError(
            f"{template_file}: expected exactly one {placeholder}, found {count}"
        )

    return rendered.replace(placeholder, fragment)


def check_unresolved_placeholders(rendered: str) -> None:
    """Raise if any template placeholders remain unresolved."""
    unresolved = sorted(set(re.findall(r"@@[A-Z0-9_]+@@", rendered)))
    if unresolved:
        raise ValueError(
            "Unresolved placeholders in template: " + ", ".join(unresolved)
        )


def render_paper(
    *,
    repo_root: Path,
    paper_dir: Path,
    build_dir: Path,
    sources_file: Path | None = None,
    template_file: Path | None = None,
    output_file: Path | None = None,
    runner: Runner = subprocess.run,
    pandoc: str = "pandoc",
    require_pandoc: bool = True,
    log: Callable[[str], None] | None = print,
) -> Path:
    """Render a complete paper supplement from a template and source manifest."""
    sources_file = sources_file or paper_dir / "sources.txt"
    template_file = template_file or paper_dir / "template.tex"
    output_file = output_file or build_dir / "rendered.tex"
    fragments_dir = build_dir / "fragments"

    if require_pandoc and shutil.which(pandoc) is None:
        raise FileNotFoundError(f"{pandoc} is not installed or not on PATH")

    if not sources_file.is_file():
        raise FileNotFoundError(f"missing {sources_file}")

    if not template_file.is_file():
        raise FileNotFoundError(f"missing {template_file}")

    sources = load_sources(sources_file, repo_root)

    build_dir.mkdir(parents=True, exist_ok=True)
    fragments_dir.mkdir(parents=True, exist_ok=True)

    rendered = template_file.read_text(encoding="utf-8")

    # Paper-specific Lua filter for the charter's authored heading numbers
    # (see build_pandoc_args); optional so papers without one are unaffected.
    lua_filter = paper_dir / "strip_heading_numbers.lua"
    if not lua_filter.is_file():
        lua_filter = None

    for key, source in sources:
        fragment_path = render_fragment(
            key,
            source,
            repo_root=repo_root,
            fragments_dir=fragments_dir,
            runner=runner,
            pandoc=pandoc,
            lua_filter=lua_filter,
            log=log,
        )
        fragment = fragment_path.read_text(encoding="utf-8")
        rendered = replace_placeholder(
            rendered,
            template_file=template_file,
            key=key,
            fragment=fragment,
        )

    check_unresolved_placeholders(rendered)
    output_file.write_text(rendered, encoding="utf-8")
    return output_file


def parse_tool_version(version_output: str, *, tool: str) -> str:
    """Extract the first whitespace-delimited version token from ``--version``
    output, e.g. ``"pandoc 3.10.1\\n..."`` -> ``"3.10.1"``."""
    match = re.search(r"(\S+)", version_output.strip())
    if match is None:
        raise ValueError(f"could not parse {tool} version from: {version_output!r}")
    return match.group(1)


def check_pandoc_version(
    *,
    runner: Runner = subprocess.run,
    pandoc: str = "pandoc",
    expected: str = PANDOC_PINNED_VERSION,
) -> str:
    """Return the installed Pandoc version, or raise if it doesn't match
    ``expected``. Reproducibility depends on this: two sandboxes used for the
    2026-10-26 audit had 3.10.1 and 2.9.2 respectively."""
    try:
        completed = runner(
            [pandoc, "--version"],
            stdout=subprocess.PIPE,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"{pandoc} --version failed") from exc
    first_line = completed.stdout.strip().splitlines()[0]
    # "pandoc 3.10.1" -> "3.10.1"
    version = parse_tool_version(first_line.removeprefix("pandoc").strip(), tool=pandoc)
    if version != expected:
        raise ValueError(
            f"{pandoc} version mismatch: found {version}, expected {expected}. "
            "The rendering pipeline is only reproducible against a pinned "
            "version; install the expected version or update "
            "PANDOC_PINNED_VERSION after reviewing the rendering diff it "
            "produces."
        )
    return version


def get_tex_engine_version(
    *, runner: Runner = subprocess.run, pdflatex: str = "pdflatex"
) -> str:
    """Return the installed pdflatex/TeX engine version string."""
    try:
        completed = runner(
            [pdflatex, "--version"],
            stdout=subprocess.PIPE,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"{pdflatex} --version failed") from exc
    return completed.stdout.strip().splitlines()[0]


def require_tool(
    name: str, *, which: Callable[[str], str | None] = shutil.which
) -> str:
    """Return the resolved path to ``name``, or raise a clear error if it
    isn't installed or on PATH."""
    path = which(name)
    if path is None:
        raise FileNotFoundError(f"{name} is not installed or not on PATH")
    return path


def check_class_file(
    class_name: str,
    *,
    runner: Runner = subprocess.run,
    kpsewhich: str = "kpsewhich",
) -> None:
    """Raise a clear error if ``class_name``'s LaTeX class isn't on the TeX
    search path. The Frontiers class file is a publisher asset that isn't
    committed to this repository pending a licensing answer (see
    WI-CHARTER-SUPPLEMENT-PDF-BUILD's Risk Notes) -- this check turns a wall
    of "Emergency stop" pdflatex log output into one actionable message."""
    if shutil.which(kpsewhich) is None:
        raise FileNotFoundError(f"{kpsewhich} is not installed or not on PATH")

    completed = runner(
        [kpsewhich, f"{class_name}.cls"],
        stdout=subprocess.PIPE,
        check=False,
        text=True,
    )
    if not completed.stdout.strip():
        raise FileNotFoundError(
            f"{class_name}.cls not found on the TeX search path. This "
            "publisher class file is not committed to the repository "
            "(licensing not confirmed for redistribution) -- supply it "
            "locally and add its directory to TEXINPUTS before running "
            "--pdf."
        )


def run_semantic_checks(
    repo_root: Path,
    *,
    runner: Runner = subprocess.run,
    python: str = sys.executable,
    modules: Sequence[str] = SEMANTIC_CHECK_MODULES,
    log: Callable[[str], None] | None = print,
) -> None:
    """Run the semantic/LaTeX regression suite before compiling a PDF, so a
    known defect class is caught before spending a pdflatex round trip on
    it."""
    if log is not None:
        log(f"Running semantic checks: {', '.join(modules)}")
    try:
        runner(
            [python, "-m", "unittest", *modules],
            cwd=repo_root,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"semantic/LaTeX regression checks failed ({', '.join(modules)})"
        ) from exc


def compile_pdf(
    tex_file: Path,
    build_dir: Path,
    *,
    runner: Runner = subprocess.run,
    pdflatex: str = "pdflatex",
    log: Callable[[str], None] | None = print,
) -> Path:
    """Compile ``tex_file`` to PDF with fail-fast flags, raising clearly
    instead of silently producing a corrupted PDF on a hard LaTeX error."""
    if log is not None:
        log(f"Compiling {tex_file.name} -> {tex_file.stem}.pdf")
    try:
        runner(
            [
                pdflatex,
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-output-directory={build_dir}",
                str(tex_file),
            ],
            cwd=build_dir,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"{pdflatex} failed compiling {tex_file} -- see "
            f"{build_dir / (tex_file.stem + '.log')} for the LaTeX log"
        ) from exc
    return build_dir / f"{tex_file.stem}.pdf"


def extract_pdf_text(
    pdf_file: Path,
    *,
    runner: Runner = subprocess.run,
    pdftotext: str = "pdftotext",
) -> str:
    """Extract PDF text with ``-layout``, using outline fonts (the template
    loads lmodern) so dashes and quotes survive extraction instead of being
    dropped by default bitmap CM fonts (see the 2026-10-26 audit)."""
    completed = runner(
        [pdftotext, "-layout", str(pdf_file), "-"],
        stdout=subprocess.PIPE,
        check=True,
        text=True,
    )
    return completed.stdout


def count_pdf_pages(pdf_text: str) -> int:
    """Count pages from ``pdftotext`` output via its form-feed page breaks."""
    if not pdf_text:
        return 0
    return pdf_text.count("\x0c") + 1


def check_pdf_text_regressions(pdf_text: str) -> list[str]:
    """Return any known corrupted substrings found in extracted PDF text.

    A regression test keyed to full-content equality would be too brittle;
    this guards against the specific glyph-loss defect class the
    2026-10-26 audit reproduced from a live pdflatex+pdftotext round trip
    with default (non-outline) fonts."""
    return [bad for bad in KNOWN_PDF_TEXT_CORRUPTIONS if bad in pdf_text]


def build_pdf(
    *,
    repo_root: Path,
    paper_dir: Path,
    build_dir: Path,
    runner: Runner = subprocess.run,
    pandoc: str = "pandoc",
    pdflatex: str = "pdflatex",
    pdftotext: str = "pdftotext",
    kpsewhich: str = "kpsewhich",
    tex_class: str = FRONTIERS_TEX_CLASS,
    skip_semantic_checks: bool = False,
    log: Callable[[str], None] | None = print,
) -> dict[str, Any]:
    """Validate sources, run semantic checks, render, and compile a PDF.

    Fails fast and clearly at the first missing/mismatched tool or asset
    rather than letting a later step (e.g. pdflatex) fail with an opaque
    log. Returns a report dict with ``pandoc_version``, ``tex_engine_version``,
    ``pdf_path``, and ``page_count``.
    """
    pandoc_version = check_pandoc_version(runner=runner, pandoc=pandoc)
    require_tool(pdflatex)
    require_tool(pdftotext)
    check_class_file(tex_class, runner=runner, kpsewhich=kpsewhich)

    if not skip_semantic_checks:
        run_semantic_checks(repo_root, runner=runner, log=log)

    tex_file = render_paper(
        repo_root=repo_root,
        paper_dir=paper_dir,
        build_dir=build_dir,
        runner=runner,
        pandoc=pandoc,
        log=log,
    )
    tex_engine_version = get_tex_engine_version(runner=runner, pdflatex=pdflatex)
    pdf_file = compile_pdf(
        tex_file, build_dir, runner=runner, pdflatex=pdflatex, log=log
    )
    pdf_text = extract_pdf_text(pdf_file, runner=runner, pdftotext=pdftotext)

    corruptions = check_pdf_text_regressions(pdf_text)
    if corruptions:
        raise RuntimeError(
            "PDF-text regression check failed: found known corrupted "
            f"substrings {corruptions!r} in extracted text -- outline fonts "
            "may not be loaded, or a dash/quote mapping regressed"
        )

    return {
        "pandoc_version": pandoc_version,
        "tex_engine_version": tex_engine_version,
        "pdf_path": pdf_file,
        "page_count": count_pdf_pages(pdf_text),
    }


def main(
    *,
    repo_root: Path,
    paper_dir: Path,
    build_dir: Path,
    argv: Sequence[str] | None = None,
) -> int:
    """CLI entry point for paper-specific shims."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pdf",
        action="store_true",
        help=(
            "validate sources, run semantic checks, render, and compile a "
            "PDF (requires pdflatex, pdftotext, and the Frontiers class "
            "file on the TeX search path)"
        ),
    )
    args = parser.parse_args(argv)

    try:
        if args.pdf:
            report = build_pdf(
                repo_root=repo_root,
                paper_dir=paper_dir,
                build_dir=build_dir,
            )
            print()
            print(f"Pandoc version: {report['pandoc_version']}")
            print(f"TeX engine version: {report['tex_engine_version']}")
            print(f"Wrote {report['pdf_path'].relative_to(repo_root)}")
            print(f"Pages: {report['page_count']}")
        else:
            output_file = render_paper(
                repo_root=repo_root,
                paper_dir=paper_dir,
                build_dir=build_dir,
            )
            print()
            print(f"Wrote {output_file.relative_to(repo_root)}")
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0
