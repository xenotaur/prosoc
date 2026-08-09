"""
Auditor orchestration logic.

This module defines the boundary between deterministic Prosoc code
and probabilistic LLM-based auditing.
"""

from __future__ import annotations

from typing import Optional, Protocol, Dict, Any
from datetime import datetime, timezone

import json
from pathlib import Path

from prosoc.auditor import validator
from prosoc.auditor import prompts
from prosoc.literate import compiler

_SCHEMA_PATH = Path(__file__).parent / "schema.json"
with _SCHEMA_PATH.open("r", encoding="utf-8") as f:
    AUDIT_REPORT_SCHEMA = json.load(f)


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


def audit_markdown_card(
    *,
    markdown_text: str,
    source_path: str,
    schema: Dict[str, Any],
    root_key: str,
    llm_client: LLMClient,
    model_name: str = "default",
) -> Dict[str, Any]:
    """
    High-level audit entry point for a Markdown normative card.

    This wrapper delegates YAML extraction and card metadata inference
    to the literate compiler using the provided schema and root key,
    then calls audit_normative_card() with explicit structured inputs.
    """

    # Delegate YAML extraction to the literate compiler
    extracted = compiler.compile_markdown(
        markdown_text,
        schema=schema,
        root_key=root_key,
    )

    if isinstance(extracted, dict) and "yaml" in extracted:
        yaml_blocks = extracted["yaml"]
    else:
        yaml_blocks = [extracted]

    if not yaml_blocks:
        raise ValueError("No YAML blocks found in Markdown card")

    # By convention, use the first YAML block
    yaml_dict = yaml_blocks[0]

    # Infer card metadata
    card_id = yaml_dict.get("id") or Path(source_path).parent.name
    card_type = yaml_dict.get("type", root_key)

    # Reference excerpts are not used in this experiment
    reference_excerpts = None

    return audit_normative_card(
        card_id=card_id,
        card_type=card_type,
        source_path=source_path,
        markdown_text=markdown_text,
        yaml_dict=yaml_dict,
        reference_excerpts=reference_excerpts,
        llm_client=llm_client,
        model_name=model_name,
    )


def audit_normative_card(
    *,
    card_id: str,
    card_type: str,
    source_path: str,
    markdown_text: str,
    yaml_dict: Dict[str, Any],
    reference_excerpts: Optional[str],
    llm_client: LLMClient,
    model_name: str = "default",
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

    system_prompt, user_prompt = prompts.build_audit_prompt(
        card_id=card_id,
        card_type=card_type,
        source_path=source_path,
        markdown_text=markdown_text,
        yaml_dict=yaml_dict,
        reference_excerpts=reference_excerpts,
        audit_report_schema=AUDIT_REPORT_SCHEMA,
    )

    # ------------------------------------------------------------
    # 2. Call LLM
    # ------------------------------------------------------------

    report = llm_client.complete(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model_name=model_name,
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
