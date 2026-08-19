#!/usr/bin/env python3

"""Render the PRNC supplementary material from Prosoc normative cards."""

from __future__ import annotations

import sys
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parent
REPO_ROOT = PAPER_DIR.parents[1]
BUILD_DIR = REPO_ROOT / "build" / "papers" / "01_charter"

sys.path.insert(0, str(REPO_ROOT / "src"))

from prosoc.nca.utils.papers import render  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(
        render.main(
            repo_root=REPO_ROOT,
            paper_dir=PAPER_DIR,
            build_dir=BUILD_DIR,
            argv=sys.argv[1:],
        )
    )
