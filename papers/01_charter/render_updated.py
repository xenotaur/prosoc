#!/usr/bin/env python3

"""Render the PRNC supplementary material from Prosoc normative cards."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path


PAPER_DIR = Path(__file__).resolve().parent
REPO_ROOT = PAPER_DIR.parents[1]

SOURCES_FILE = PAPER_DIR / "sources.txt"
TEMPLATE_FILE = PAPER_DIR / "template.tex"

BUILD_DIR = REPO_ROOT / "build" / "papers" / "01_charter"
FRAGMENTS_DIR = BUILD_DIR / "fragments"
OUTPUT_FILE = BUILD_DIR / "rendered.tex"


def load_sources() -> list[tuple[str, Path]]:
    sources: list[tuple[str, Path]] = []

    for line_number, raw_line in enumerate(
        SOURCES_FILE.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(
                f"{SOURCES_FILE}:{line_number}: expected 'KEY path'"
            )

        key, relative_path = parts
        source = REPO_ROOT / relative_path

        if not source.is_file():
            raise FileNotFoundError(
                f"{SOURCES_FILE}:{line_number}: source does not exist: {source}"
            )

        sources.append((key, source))

    return sources


def render_fragment(key: str, source: Path) -> Path:
    filename = f"{key.lower()}.tex"
    output = FRAGMENTS_DIR / filename

    print(f"Rendering {source.relative_to(REPO_ROOT)} -> "
          f"{output.relative_to(REPO_ROOT)}")

    pandoc_args = [
        "pandoc",
        "-f",
        "markdown",
        "-t",
        "latex",
    ]

    # The charter is a top-level section in the supplement. All other
    # normative cards are inserted beneath hand-authored category sections
    # in template.tex, so shift their Markdown heading hierarchy down by one.
    if key != "CHARTER":
        pandoc_args.append("--shift-heading-level-by=1")

    # Always append the source path after any per-source options. Keeping this
    # outside the conditional is important: if Pandoc is invoked without an
    # input file, it reads stdin and can appear to hang.
    pandoc_args.append(str(source))

    with output.open("w", encoding="utf-8") as stream:
        subprocess.run(
            pandoc_args,
            cwd=REPO_ROOT,
            stdin=subprocess.DEVNULL,
            stdout=stream,
            check=True,
        )

    return output


def main() -> int:
    if shutil.which("pandoc") is None:
        print("error: pandoc is not installed or not on PATH", file=sys.stderr)
        return 1

    if not SOURCES_FILE.is_file():
        print(f"error: missing {SOURCES_FILE}", file=sys.stderr)
        return 1

    if not TEMPLATE_FILE.is_file():
        print(f"error: missing {TEMPLATE_FILE}", file=sys.stderr)
        return 1

    sources = load_sources()

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    FRAGMENTS_DIR.mkdir(parents=True, exist_ok=True)

    rendered = TEMPLATE_FILE.read_text(encoding="utf-8")

    for key, source in sources:
        placeholder = f"@@{key}@@"

        count = rendered.count(placeholder)
        if count != 1:
            raise ValueError(
                f"{TEMPLATE_FILE}: expected exactly one {placeholder}, "
                f"found {count}"
            )

        fragment_path = render_fragment(key, source)
        fragment = fragment_path.read_text(encoding="utf-8")

        rendered = rendered.replace(placeholder, fragment)

    unresolved = sorted(set(re.findall(r"@@[A-Z0-9_]+@@", rendered)))
    if unresolved:
        raise ValueError(
            "Unresolved placeholders in template: "
            + ", ".join(unresolved)
        )

    OUTPUT_FILE.write_text(rendered, encoding="utf-8")

    print()
    print(f"Wrote {OUTPUT_FILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
