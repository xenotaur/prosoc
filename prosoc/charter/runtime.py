"""
runtime.py

Runtime (Python-facing) representation of the Prosocial Robot Navigation Charter.

This module defines Pydantic models used by downstream code (evaluators,
strategizers, planners, etc.) to *consume* a validated charter.

IMPORTANT:
- This module is NOT the source of truth for the charter structure.
- Structural validity is defined by `schema.json` and enforced during loading.
- These models exist for typing, ergonomics, and runtime convenience only.
"""

import pathlib
from typing import List, Optional

import pydantic


# -----------------------------------------------------------------------------
# Runtime models
# -----------------------------------------------------------------------------

class ExampleSet(pydantic.BaseModel):
    """
    Illustrative examples associated with a charter principle.

    These are assumed to be structurally validated upstream by JSON Schema.
    """

    positive: List[str]
    negative: List[str]


class CharterPrinciple(pydantic.BaseModel):
    """
    Runtime representation of a single prosocial navigation principle.

    This model intentionally mirrors (but does not define) the normative
    structure specified in `schema.json`.
    """

    id: str
    name: str
    description: str
    severity: str
    examples: ExampleSet

    # ------------------------------------------------------------------
    # Convenience helpers (non-normative)
    # ------------------------------------------------------------------

    def is_hard_constraint(self) -> bool:
        """
        Returns True if violations of this principle should be treated
        as hard failures by downstream systems.
        """
        return self.severity in {"critical", "high"}

    def is_soft_constraint(self) -> bool:
        """
        Returns True if violations of this principle may be traded off
        against other considerations.
        """
        return self.severity in {"medium", "optional"}


class Charter(pydantic.BaseModel):
    """
    Runtime container for the full prosocial navigation charter.

    This object is typically constructed by `loader.load_charter()` after
    schema validation has already succeeded.
    """

    principles: List[CharterPrinciple]

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------

    def by_id(self, principle_id: str) -> Optional[CharterPrinciple]:
        """
        Retrieve a principle by its ID (e.g., "P1").

        Returns None if no such principle exists.
        """
        for principle in self.principles:
            if principle.id == principle_id:
                return principle
        return None

    def hard_constraints(self) -> List[CharterPrinciple]:
        """
        Return all principles considered hard constraints.
        """
        return [p for p in self.principles if p.is_hard_constraint()]

    def soft_constraints(self) -> List[CharterPrinciple]:
        """
        Return all principles considered soft constraints.
        """
        return [p for p in self.principles if p.is_soft_constraint()]
