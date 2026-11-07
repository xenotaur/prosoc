---
family: charter
card: charter
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-11-07
---

# Audit: Prosocial Robot Navigation Charter

- **Card:** `src/prosoc/prnc/charter/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED with minor fixes — one should-fix item (a
  recurring Normative-Statement/description drift), no blocking issues.

## Findings

### 1. Normative Statement omits content the YAML `description` and prose Explanation carry — should-fix
- **Section/field:** Prose `### Normative Statement` vs. embedded YAML `description` (P1, P2, P4, P5, and to a lesser extent P6)
- **Issue:** For several principles, the terse `### Normative Statement` subsection
  no longer states the full normative content that the embedded YAML
  `description` field carries (and that the `### Explanation` subsection
  elaborates). Concretely:
  - **P1 Safety:** Normative Statement reads "Robots must not cause harm to
    humans, or damage to other robots, environments, or themselves." The YAML
    `description` adds "This includes maintaining a safe distance unless
    explicitly invited to approach." — present in the Explanation but not in
    the headline statement.
  - **P2 Comfort:** Normative Statement omits the description's "This includes
    refraining from sudden movements or uninvited approaches."
  - **P4 Politeness:** Normative Statement says "...toward other agents in
    shared social spaces," while the YAML `description` instead emphasizes
    "...offering help when asked and avoiding dismissive or intrusive
    behaviors" — the two statements foreground different content rather than
    one simply being a subset of the other.
  - **P5 Social Competency:** similarly, the Normative Statement's "governing
    shared spaces" framing and the YAML description's "avoiding inappropriate
    behaviors such as interrupting conversations or blocking passage" diverge
    in emphasis.
  - **P6 Agent Understanding** (minor): the YAML description's parenthetical
    "(humans, robots, pets, etc.)" has no counterpart in the Normative
    Statement.

  This is drift rather than contradiction — nothing here is factually
  incompatible, and `scripts/distill/charter --dry-run --show-diffs` reports
  no diff, so this is not a tooling-freshness issue. It traces to the
  2026-08-06 EDITED entry that explicitly "fold[ed] P1/P4/P5's YAML-only
  `description` content ... into their prose Explanations" without
  back-porting the same content into the terse Normative Statement headline.
  A reader who only skims the Normative Statement (the subsection the
  Definitions and Glossary section calls "the primary reference point for
  interpretation and enforcement") would miss normatively real content for
  four of ten principles.
- **Recommended fix:** For P1, P2, P4, P5 (and optionally P6), either fold the
  extra clause back into the Normative Statement itself, or add an explicit
  note that the YAML `description` is the fuller operative text and the
  Normative Statement is deliberately a headline summary. Either is
  acceptable; leaving the asymmetry undocumented is the actual gap.

### Considered and rejected: `principles.md`'s P9 summary row

An earlier draft of this audit flagged `../_shared/principles.md`'s P9
summary row ("...without sacrificing own goals or task/context fit") as
should-fix stale wording, reasoning that the charter's 2026-08-19
WI-CHARTER-FRONTIERS-SYNC edit "trimmed" this qualifier from P9's
Normative Statement. **Caught in review and corrected:** the charter's own
P9 Explanation states the qualifier explicitly remains operative —
"even though its normative statement no longer restates the limit
explicitly, P9 still cannot be read in isolation from P0 and P8 — that
bound is expressed here, in this Explanation, rather than in the statement
itself." `principles.md`'s own header says it is a one-line *summary* per
principle, not a transcription of the Normative Statement specifically,
and instructs the reader to verify against the charter if the two "ever
appear to disagree" — which, read in full (statement + Explanation), they
do not. Retaining the qualifier in the summary is accurate, not stale;
this is not a finding.

### 2. P4 and P5 positive examples both illustrate "yielding to people passing" — suggestion
- **Section/field:** P4 Politeness `examples.positive` vs. P5 Social Competency `examples.positive`
- **Issue:** P4's "Robot pauses to let two people pass during their
  conversation" and P5's "Robot waits at the side while people pass in a
  narrow hallway" both depict a robot yielding so people can pass. They are
  not interchangeable on close reading — P4's is about not interrupting a
  conversation (an individual-courtesy angle) while P5's is about following a
  narrow-space queueing norm — but the surface similarity is close enough
  that a reader skimming examples alone could conflate the two principles.
- **Recommended fix:** No action required; optionally sharpen one example's
  wording (e.g., naming the conversational-interruption angle explicitly in
  P4's example) to make the distinction more self-evident without relying on
  the surrounding prose.

## Completeness

- All ten principles (P0–P9) have every schema-required field (`id`, `name`,
  `description`, `severity`, non-empty `examples.positive`/`.negative`) — no
  blanks found.
- All structural sections required by the checklist are present: `## Status`,
  `## 1. Purpose of This Charter`, `## 2. Definition...`, `## 3. Structure of
  the Principles`, `## 14. Use of This Charter...`, `## Definitions and
  Glossary`, and `## References`.
- Nothing is reasonably-blank or should-fill-in-now — the charter document is
  complete per both the schema and the structural checklist.
