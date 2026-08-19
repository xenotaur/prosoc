"""Exceptions for the normative packet assembler."""

from __future__ import annotations


class PacketError(Exception):
    """Base class for all packet-assembly failures."""


class ManifestError(PacketError):
    """The manifest is malformed or names an unknown family."""


class ResolveError(PacketError):
    """A manifest member does not resolve to a card, or fails to load."""


class GateError(PacketError):
    """The lifecycle gate blocked assembly (fail-closed)."""


class AssembleError(PacketError):
    """The assembled envelope could not be built or failed schema validation."""
