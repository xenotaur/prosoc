"""CLI: assemble a normative guidance packet from a manifest.

Run via ``scripts/assemble`` (a thin wrapper around
``python -m prosoc.packet.cli``). Fail-closed: if any member is below the gate
threshold the command prints why and emits **nothing**.

    scripts/assemble <manifest.yml>
    scripts/assemble <manifest.yml> --allow-unapproved "dev packet for testing"
    scripts/assemble <manifest.yml> --allow-unapproved "..." --check
"""

from __future__ import annotations

import argparse
import difflib
import json
import pathlib
import sys

import yaml

from .assemble import assemble
from .errors import PacketError
from .gate import gate
from .manifest import load_manifest
from .resolve import resolve

GOLDEN_FILENAME = "packet.golden.yml"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Assemble a normative guidance packet from a manifest."
    )
    parser.add_argument("manifest", help="Path to the manifest YAML file.")
    parser.add_argument(
        "--allow-unapproved",
        metavar="JUSTIFICATION",
        default=None,
        help=(
            "Lower the lifecycle gate below APPROVED and stamp a non-production "
            "marker into the packet. Requires a written justification."
        ),
    )
    parser.add_argument(
        "--format",
        choices=["yaml", "json"],
        default="yaml",
        help="Output serialization for the assembled packet (default: yaml).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Assemble as usual, then byte-compare the rendered packet against "
            f"<manifest_dir>/{GOLDEN_FILENAME} instead of printing it. Exits 0 "
            "silently on a match, 1 with a unified diff on stderr on drift, or "
            "1 with an error if no golden file exists yet."
        ),
    )
    args = parser.parse_args(argv)

    if args.check and args.format == "json":
        print(
            "error: --check compares against a YAML golden file "
            f"({GOLDEN_FILENAME}); --format json is not supported with --check",
            file=sys.stderr,
        )
        return 2

    allow = args.allow_unapproved is not None
    if allow and not args.allow_unapproved.strip():
        print(
            "error: --allow-unapproved requires a non-empty justification",
            file=sys.stderr,
        )
        return 2

    try:
        manifest = load_manifest(pathlib.Path(args.manifest))
        cards = resolve(manifest)
        result = gate(cards, allow_unapproved=allow)
        if not result.passed:
            print(
                f"packet blocked (fail-closed, threshold {result.threshold}); "
                "nothing emitted:",
                file=sys.stderr,
            )
            for b in result.blocked:
                print(f"  - {b.family}/{b.id}: {b.reason}", file=sys.stderr)
            return 1
        envelope = assemble(
            cards,
            manifest,
            allow_unapproved=allow,
            justification=args.allow_unapproved,
        )
    except PacketError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        rendered = json.dumps(envelope, indent=2, ensure_ascii=False) + "\n"
    else:
        rendered = yaml.safe_dump(envelope, sort_keys=False, allow_unicode=True)

    if args.check:
        return _check(rendered, pathlib.Path(args.manifest))

    print(rendered, end="")
    return 0


def _check(rendered: str, manifest_path: pathlib.Path) -> int:
    golden_path = manifest_path.parent / GOLDEN_FILENAME
    try:
        golden_text = golden_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(
            f"error: no golden packet at {golden_path}\n"
            "Create one by redirecting a normal run, e.g.:\n"
            f'  scripts/assemble {manifest_path} --allow-unapproved "<justification>" '
            f"> {golden_path}",
            file=sys.stderr,
        )
        return 1

    if rendered == golden_text:
        return 0

    diff = difflib.unified_diff(
        golden_text.splitlines(keepends=True),
        rendered.splitlines(keepends=True),
        fromfile=str(golden_path),
        tofile="<assembled>",
    )
    sys.stderr.writelines(diff)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
