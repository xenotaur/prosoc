"""
errors.py

Exception hierarchy for literate Markdown compilation.

These errors represent *author-facing* or *pipeline-level* failures
and are intended to be caught by CLI tools, CI checks, or tests.
"""


class LiterateError(Exception):
    """
    Base class for all literate compilation errors.
    """

    pass


class LiterateSourceError(LiterateError):
    """
    Raised when the Markdown source is missing required structure,
    such as fenced YAML blocks.
    """

    pass


class LiterateYamlError(LiterateError):
    """
    Raised when a fenced YAML block cannot be parsed as valid YAML.
    """

    pass


class LiterateStructureError(LiterateError):
    """
    Raised when parsed YAML is syntactically valid but structurally invalid,
    e.g., not a mapping or missing required keys prior to schema validation.
    """

    pass


class LiterateSchemaError(LiterateError):
    """
    Raised when a document fails JSON Schema validation.
    """

    pass


class LiterateIOError(LiterateError):
    """
    Raised for file I/O or atomic write failures in literate tooling.
    """

    pass


class LiterateDiscoveryError(LiterateError):
    """
    Raised when source discovery finds no matching documents under a root,
    e.g. an empty corpus or an unmatched single-item filter.
    """

    pass
