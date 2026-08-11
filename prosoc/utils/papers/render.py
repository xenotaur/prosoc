"""Render paper supplements from Markdown card sources."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

PANDOC_HORIZONTAL_RULE = "\\begin{center}\\rule{0.5\\linewidth}{0.5pt}\\end{center}"
SOURCE_KEY_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")

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


def build_pandoc_args(key: str, source: Path, *, pandoc: str = "pandoc") -> list[str]:
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
        build_pandoc_args(key, source, pandoc=pandoc),
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

    for key, source in sources:
        fragment_path = render_fragment(
            key,
            source,
            repo_root=repo_root,
            fragments_dir=fragments_dir,
            runner=runner,
            pandoc=pandoc,
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


def main(
    *,
    repo_root: Path,
    paper_dir: Path,
    build_dir: Path,
    argv: Sequence[str] | None = None,
) -> int:
    """CLI entry point for paper-specific shims."""
    if argv:
        print("error: this renderer takes no arguments", file=sys.stderr)
        return 2

    try:
        output_file = render_paper(
            repo_root=repo_root,
            paper_dir=paper_dir,
            build_dir=build_dir,
        )
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print()
    print(f"Wrote {output_file.relative_to(repo_root)}")
    return 0
