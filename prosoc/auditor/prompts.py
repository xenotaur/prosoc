"""
Prompt construction utilities for the Prosoc auditor.

This module builds deterministic, schema-aligned prompts for auditing
Normative Cards using an LLM. It does *not* perform any LLM calls itself.
"""

from __future__ import annotations

import json
from textwrap import dedent
from typing import Any, Dict, Optional, Tuple

SYSTEM_PROMPT = dedent("""
    You are a meticulous technical auditor.

    Your task is to audit a structured normative specification by checking
    whether a machine-readable YAML representation faithfully matches the
    human-readable Markdown description, and optionally whether it is
    consistent with a provided reference document.

    You must be conservative, evidence-based, and precise.

    If an issue cannot be clearly justified using quoted or paraphrased
    evidence from the provided materials, do not report it.
    """).strip()


USER_PROMPT_TEMPLATE = dedent("""
    You are auditing a Prosoc Normative Card.

    Your task has three phases:

    PHASE 1 — INTERNAL CONSISTENCY
    Check whether the extracted YAML accurately and completely reflects
    the meaning expressed in the Markdown description.

    PHASE 2 — REFERENCE CONSISTENCY (if reference material is provided)
    Check whether the YAML content is consistent with the provided reference
    document (e.g., definitions, constraints, or principles).

    PHASE 3 — REPORT
    Produce a structured audit report as JSON that conforms exactly to the
    provided JSON Schema.

    IMPORTANT RULES:
    - Treat the Markdown prose as normative.
    - Treat the YAML as an implementation to be audited.
    - Do NOT propose new content.
    - Do NOT rewrite the YAML.
    - Do NOT speculate.
    - If information is missing or ambiguous, mark the result as "uncertain".
    - Every reported issue MUST cite evidence.
    - If no issues are found, report empty issue lists.

    You MUST output only JSON. No explanations, no markdown, no comments.

    ------------------------------------------------------------
    INPUTS
    ------------------------------------------------------------

    [A] CARD METADATA
    Card ID: {card_id}
    Card Type: {card_type}
    Source Path: {source_path}

    [B] MARKDOWN DESCRIPTION (NORMATIVE SOURCE)
    {markdown_text}

    [C] EXTRACTED YAML (IMPLEMENTATION UNDER REVIEW)
    The following is a canonical JSON rendering of the extracted YAML:

    {yaml_as_json}

    [D] REFERENCE MATERIAL (OPTIONAL)
    If present, this material is normative for reference consistency checks.
    If not present, reference consistency must be marked as "not_evaluated".

    {reference_excerpts}

    ------------------------------------------------------------
    OUTPUT REQUIREMENTS
    ------------------------------------------------------------

    You must output a single JSON object that conforms EXACTLY to this schema:

    {audit_report_schema}

    Additional constraints:
    - audit_metadata.timestamp must be an ISO 8601 UTC timestamp.
    - audit_metadata.audit_version must be "0.1".
    - internal_consistency.status must be:
      - "pass" if no internal issues are found
      - "fail" if one or more errors are found
      - "uncertain" if ambiguity prevents a clear judgment
    - reference_consistency.status must be:
      - "not_evaluated" if no reference material was provided
      - otherwise "pass", "fail", or "uncertain"
    - summary counts must match the number of issues reported.
    - confidence should reflect your certainty in the audit.

    Do not include fields that are not in the schema.
    Do not omit required fields.
    """).strip()


def build_audit_prompt(
    *,
    card_id: str,
    card_type: str,
    source_path: str,
    markdown_text: str,
    yaml_dict: Dict[str, Any],
    reference_excerpts: Optional[str],
    audit_report_schema: Dict[str, Any],
) -> Tuple[str, str]:
    """
    Build the system and user prompts for auditing a normative card.

    Parameters
    ----------
    card_id : str
        Unique identifier of the card.
    card_type : str
        Type of card (e.g., "scenario", "task", "principle").
    source_path : str
        Filesystem or repository path of the card.
    markdown_text : str
        Human-readable normative Markdown text.
    yaml_dict : dict
        Extracted YAML content as a Python dictionary.
    reference_excerpts : str or None
        Reference material for cross-checking, or None.
    audit_report_schema : dict
        JSON Schema the output must conform to.

    Returns
    -------
    (system_prompt, user_prompt) : tuple of str
        Prompts suitable for submission to an LLM.
    """

    yaml_as_json = json.dumps(yaml_dict, indent=2, sort_keys=False)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        card_id=card_id,
        card_type=card_type,
        source_path=source_path,
        markdown_text=markdown_text.strip(),
        yaml_as_json=yaml_as_json,
        reference_excerpts=(reference_excerpts or "<none>"),
        audit_report_schema=json.dumps(audit_report_schema, indent=2),
    )

    return SYSTEM_PROMPT, user_prompt
