# prosoc/utils/auditor/markdown_validator.py

from typing import Dict, Any
from prosoc.literate import compiler


def validate_markdown_card(
    *,
    markdown_text: str,
    schema: Dict[str, Any],
    root_key: str,
) -> Dict[str, Any]:
    """
    Validate a Markdown normative card by attempting schema-driven
    YAML extraction via the literate compiler.
    """

    try:

        extracted = compiler.compile_markdown(
            markdown_text,
            schema=schema,
            root_key=root_key,
        )

        # Normalize compiler output
        if isinstance(extracted, dict) and "yaml" in extracted:
            yaml_blocks = extracted["yaml"]
        else:
            # Unrooted single-card case: compiler returns the YAML mapping directly
            yaml_blocks = [extracted]

        if not yaml_blocks:
            return {
                "valid": False,
                "stage": "yaml_extraction",
                "error": "No YAML blocks found",
            }

        return {
            "valid": True,
            "yaml_count": len(yaml_blocks),
        }

    except Exception as e:
        return {
            "valid": False,
            "stage": "compile",
            "error": str(e),
        }
