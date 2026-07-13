"""
Utilities for mutating normative cards for experimental purposes.

This module intentionally operates on Markdown-with-embedded-YAML,
which is the auditable artifact in the Prosoc architecture.
"""

from __future__ import annotations

import yaml


class YamlBlockNotFoundError(ValueError):
    """Raised when no YAML fenced block is found in a Markdown document."""


class MultipleYamlBlocksError(ValueError):
    """Raised when more than one YAML fenced block is found."""


def replace_yaml_block(markdown_text: str, new_yaml_dict: dict) -> str:
    """
    Replace the embedded YAML block in a Markdown normative card
    with a new YAML specification.

    Parameters
    ----------
    markdown_text : str
        Original Markdown text containing exactly one ```yaml fenced block.
    new_yaml_dict : dict
        New YAML content to embed.

    Returns
    -------
    str
        Markdown text with the YAML block replaced.

    Raises
    ------
    YamlBlockNotFoundError
        If no YAML fenced block is found.
    MultipleYamlBlocksError
        If more than one YAML fenced block is found.
    """

    fence_start = "```yaml"
    fence_end = "```"

    start_idx = markdown_text.find(fence_start)
    if start_idx == -1:
        raise YamlBlockNotFoundError("No ```yaml fenced block found.")

    end_idx = markdown_text.find(
        fence_end,
        start_idx + len(fence_start),
    )
    if end_idx == -1:
        raise YamlBlockNotFoundError("YAML fenced block not properly closed.")

    # Check for multiple YAML blocks
    second_start = markdown_text.find(
        fence_start,
        end_idx + len(fence_end),
    )
    if second_start != -1:
        raise MultipleYamlBlocksError("Multiple ```yaml fenced blocks found.")

    # Serialize new YAML
    Dumper = getattr(yaml, 'CSafeDumper', yaml.SafeDumper)
    new_yaml_text = yaml.dump(
        new_yaml_dict,
        Dumper=Dumper,
        sort_keys=False,
        default_flow_style=False,
    ).rstrip()

    # Reconstruct Markdown
    before = markdown_text[:start_idx]
    after = markdown_text[end_idx + len(fence_end) :]

    replaced = before + fence_start + "\n" + new_yaml_text + "\n" + fence_end + after

    return replaced
