"""
Auditor orchestration logic.

This module defines the boundary between deterministic Prosoc code
and probabilistic LLM-based auditing.
"""

from __future__ import annotations

from typing import Optional, Protocol, Dict, Any
from datetime import datetime, timezone
import json

from prosoc.auditor import validator
from prosoc.auditor.prompts import build_audit_prompt


class LLMClient(Protocol):
    """
    Minimal protocol for an LLM client usable by the auditor.

    This allows the auditor to be tested with a mock or fake LLM.
    """

    def audit(self, *, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Perform an audit call and return parsed JSON output.

        Must return a Python dict corresponding to the audit report.
        """
        ...


def audit_normative_card(
    *,
    card_id: str,
    card_type: str,
    source_path: str,
    markdown_text: str,
    yaml_dict: Dict[str, Any],
    reference_excerpts: Optional[str],
    llm_client: LLMClient,
    model_name: str,
) -> Dict[str, Any]:
    """
    Orchestrate an audit of a Prosoc normative card.

    Parameters
    ----------
    card_id : str
        Unique identifier of the card.
    card_type : str
        Type of card (e.g. "scenario", "task", "principle").
    source_path : str
        Path to the source Markdown file.
    markdown_text : str
        Human-readable normative Markdown (excluding YAML blocks).
    yaml_dict : dict
        Extracted YAML content as a Python dict.
    reference_excerpts : str or None
        Retrieved reference material (e.g. from P&G paper), or None.
    llm_client : LLMClient
        Client responsible for executing the LLM audit call.
    model_name : str
        Identifier of the LLM model being used.

    Returns
    -------
    dict
        Validated audit report.

    Raises
    ------
    jsonschema.ValidationError
        If the LLM output does not conform to the audit report schema.
    """

    # ------------------------------------------------------------
    # 1. Build prompts
    # ------------------------------------------------------------

    system_prompt, user_prompt = build_audit_prompt(
        card_id=card_id,
        card_type=card_type,
        source_path=source_path,
        markdown_text=markdown_text,
        yaml_dict=yaml_dict,
        reference_excerpts=reference_excerpts,
        model_name=model_name,
    )

    # ------------------------------------------------------------
    # 2. Call LLM
    # ------------------------------------------------------------

    report = llm_client.audit(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    # ------------------------------------------------------------
    # 3. Enforce required audit metadata fields
    #    (LLMs sometimes omit timestamps even when instructed)
    # ------------------------------------------------------------

    if "audit_metadata" in report:
        report["audit_metadata"].setdefault(
            "timestamp",
            datetime.now(timezone.utc).isoformat(),
        )
        report["audit_metadata"].setdefault("model", model_name)
        report["audit_metadata"].setdefault("audit_version", "0.1")

    # ------------------------------------------------------------
    # 4. Validate against schema
    # ------------------------------------------------------------

    validator.validate_audit_report(report)

    return report
