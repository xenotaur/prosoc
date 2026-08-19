"""Backwards-compat shim: scenarios-only entry to the card status validator.

The generalized, family-aware validator lives in
``prosoc.nca.utils.cards.validate_status`` (see ``WI-CARD-STATUS-TASKS``). This
module forces the ``scenarios`` family and forwards the remaining arguments, so
existing ``from prosoc.prnc.scenarios import validate_status`` call sites and tests
(which pass ``--root`` / ``--layout`` / ``--fix``) keep working unchanged.
"""

from __future__ import annotations

from prosoc.nca.utils.cards import validate_status as _generic


def main(argv: list[str] | None = None) -> int:
    return _generic.main(["--family", "scenarios", *(argv or [])])


if __name__ == "__main__":
    raise SystemExit(main())
