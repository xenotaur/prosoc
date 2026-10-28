---
id: WS-CHARTER-SUPPLEMENT-PIPELINE
kind: planning_node
title: "Charter Supplementary-Material Pipeline Repair"
status: proposed
stage: planned
origin: ad_hoc
summary: "Repair and harden the Frontiers charter-supplement rendering pipeline (papers/01_charter): fix source-card and renderer defects, add regression tests, build a reproducible PDF build entry point, wire CI, and regenerate the golden file -- grounded in a dual-pass audit of an external handoff's claims."
related_focus: []
related_roadmap: []
related_design:
  - project/design/proposals/adopted/charter-frontiers-sync/00_proposal.md
work_items:
  - WI-CHARTER-SUPPLEMENT-SOURCE-FIXES
  - WI-CHARTER-LIFECYCLE-DISPLAY-FIX
  - WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK
  - WI-CHARTER-SUPPLEMENT-RENDERER-FIXES
  - WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION
  - WI-CHARTER-SUPPLEMENT-TEST-COVERAGE
  - WI-CHARTER-SUPPLEMENT-PDF-BUILD
  - WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN
  - WI-CHARTER-SUPPLEMENT-CI
evidence:
  - project/audits/2026-10-26_charter_supplement_pipeline_audit.md
exit_criteria:
  - "papers/01_charter's 9 source cards are free of the stale pre-restructure paths, collapsed-list formatting, and dangling cross-references identified in the 2026-10-26 audit"
  - "No card's state: field or the charter's APPROVED status is changed; the charter's Status: header and edit history are reconciled with its authoritative STATE instead"
  - "scripts/validate/status checks each card's audit.md existence/verdict, not the optional AUDITED: provenance bullet"
  - "The Frontiers template/renderer no longer double-numbers charter headings or loses Unicode punctuation inside lstlisting blocks (verified in compiled-PDF text, not just .tex)"
  - "A reproducible PDF build entry point exists with a pinned/checked Pandoc version, and papers/01_charter/golden/rendered.tex is regenerated only after a human reviews the resulting content diff"
  - "CI exercises the supplement pipeline (render, golden diff, PDF compile where assets are available) on changes to papers/01_charter/** and its 9 sources"
---

# Charter Supplementary-Material Pipeline Repair

## Purpose

Coordinates the repair of the Frontiers charter-supplement rendering
pipeline under `papers/01_charter/`, following a dual-pass audit
(`project/audits/2026-10-26_charter_supplement_pipeline_audit.md`) that
verified an external handoff's 13 claimed defects against the repo. Most
claims held up; the most consequential one didn't as originally framed —
the charter's `APPROVED` lifecycle state is legitimately earned, not stale
— so this workstream exists to land the *correct* version of the fixes,
not the handoff verbatim.

## Scope

- Source-card text fixes: collapsed-list formatting, stale pre-restructure
  paths, a leaked internal tooling path, an internal-attribution string,
  and a dangling cross-reference, across the 9 cards included in the
  supplement.
- A display-only fix to the charter's stale `Status:` header and its
  edit-history bullets — explicitly not a lifecycle-state change.
- A `scripts/validate/status` enhancement so lifecycle validation checks
  real audit evidence (`audit.md`) rather than an optional provenance
  bullet.
- Renderer/template fixes: a charter-scoped Lua filter for heading
  numbers, Unicode `literate=` mappings for the `listings` package,
  identifier formatting normalization.
- New regression tests for each of the above, plus a semantic YAML
  round-trip check.
- A reproducible PDF build entry point with a pinned/checked Pandoc
  version.
- Golden-file regeneration, gated on a human content-diff review.
- CI coverage for the whole pipeline.

## Prior Art Check

### Duplication search
- In-repo: no existing workstream or open proposal covers this scope.
  `WI-PAPER-RENDERER-TESTABLE-CORE` (resolved, PR #89) built the
  renderer core this workstream extends; `WI-CHARTER-FRONTIERS-SYNC`
  (resolved, PR #97) is the charter edit whose aftermath (stale golden
  file, stale Status: header) this workstream addresses.
- Sibling repos / external libraries: none identified — this is
  prosoc/Frontiers-specific tooling.
- Recommendation: Proceed.

### Demand search
- Work items: none found referencing `papers/01_charter` or "supplement"
  beyond the two resolved items above.
- Proposals: none found proposing this repair.
- Backlog: no matching entries in `project/design/backlog.md`.
- Recommendation: No action — this is new demand, captured by the
  2026-10-26 audit rather than a pre-existing backlog entry.

## Work Items

- **WI-CHARTER-SUPPLEMENT-SOURCE-FIXES** — Fix collapsed-list formatting
  (blank lines before lists after bold labels), stale `prosoc/...`
  pre-restructure paths (`charter.md:28`, two scenario cards), the
  `.claude/skills/...` reference, the `SOURCE: Prompt to ChatGPT 5.2`
  string, the dangling `blind_corner` reference, Task-ID/Context-ID
  code-span inconsistency, and `papers/01_charter/README.md`'s stale
  import path.
- **WI-CHARTER-LIFECYCLE-DISPLAY-FIX** — Fix `charter.md:4`'s stale
  `Status:` header and add the missing closing history bullet(s). Does
  not touch `state:`.
- **WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK** — Extend
  `scripts/validate/status` to check each card's sibling `audit.md`
  existence/verdict and the charter's free-text `Status:` line against
  its authoritative `STATE`.
- **WI-CHARTER-SUPPLEMENT-RENDERER-FIXES** — Charter-scoped Lua filter
  for heading numbers; `literate=` Unicode mappings on the
  `literatecard` style; identifier code-span normalization.
- **WI-CHARTER-SUPPLEMENT-TEST-COVERAGE** — Regression tests: list-collapse
  (keyed on pattern, not a literal bolded string), heading-number-once,
  YAML semantic round-trip, identifier survival through render + PDF text.
- **WI-CHARTER-SUPPLEMENT-PDF-BUILD** — `render.py --pdf`/`--check` (or a
  new build-entrypoint script): `pdflatex` with fail-fast flags and
  outline fonts, `pdftotext -layout` checks, pinned/checked Pandoc version.
- **WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN** — Regenerate
  `golden/rendered.tex` after the above land, with a mandatory manual
  content-diff review (golden predates PR #97's charter content).
  Depends on the renderer, test, and PDF-build items.
- **WI-CHARTER-SUPPLEMENT-CI** — Workflow triggered on
  `papers/01_charter/**` and its 9 sources: render, golden diff, PDF
  compile/text checks when assets are available. Depends on the
  PDF-build item.

## Exit Criteria

See frontmatter `exit_criteria`.

## Non-Goals

- Does not change any normative card's `state:` field, including the
  charter's.
- Does not resolve the editorial/content-review items from the original
  handoff (`must`/`should` wording, P9 definitional alignment, PDF
  metadata, page-layout polish) — those stay human-judgment follow-ups,
  out of scope here.
- Does not commit third-party Frontiers publisher assets without
  confirming licensing permits it.

## Open Questions

- Whether the PDF build entry point is a new `render.py` flag or a
  separate `scripts/build-paper-supplement` script — left to
  `WI-CHARTER-SUPPLEMENT-PDF-BUILD`'s implementation.
