"""Normative packet assembler engine (Phase 1).

Turns a human-authored manifest naming member cards into a single
machine-readable guidance packet: load (``loader``) -> resolve (``resolve``) ->
lifecycle gate (``gate``) -> assemble into a namespaced, in-toto-style
provenance envelope (``assemble``), validated against ``schema.json``.

See ``project/design/proposals/proposed/normative-packet-assembly/00_proposal.md``
(Decisions 2, 4, 5, 6; Implementation Plan Phase 1).
"""
