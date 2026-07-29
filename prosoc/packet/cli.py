"""CLI: assemble a normative guidance packet from a manifest.

Run via ``scripts/assemble`` (a thin wrapper around
``python -m prosoc.packet.cli``). Fail-closed: if any member is below the gate
threshold the command prints why and emits **nothing**.

    scripts/assemble <manifest.yml>
    scripts/assemble <manifest.yml> --allow-unapproved "dev packet for testing"
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import yaml

from .assemble import assemble
from .errors import PacketError
from .gate import gate
from .manifest import load_manifest
from .resolve import resolve


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
    args = parser.parse_args(argv)

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
        print(json.dumps(envelope, indent=2, ensure_ascii=False))
    else:
        print(yaml.safe_dump(envelope, sort_keys=False, allow_unicode=True), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
