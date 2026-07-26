"""
Scenario lifecycle-state helpers.

The implementation now lives in the family-agnostic shared module
``prosoc.utils.cards.status`` (see ``WI-CARD-STATUS-TASKS``). This module is a
thin re-export kept for backwards compatibility so existing
``from prosoc.scenarios import status`` call sites and tests keep working.
"""

from __future__ import annotations

from prosoc.utils.cards.status import (
    STATES,
    ConsistencyResult,
    StatusStateError,
    check_consistency,
    check_source,
    parse_markdown_state,
    project_state_into_markdown,
    read_yaml_state,
)

__all__ = [
    "STATES",
    "ConsistencyResult",
    "StatusStateError",
    "check_consistency",
    "check_source",
    "parse_markdown_state",
    "project_state_into_markdown",
    "read_yaml_state",
]
