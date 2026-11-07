---
family: charter
card: charter
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 1
audited: 2026-11-07
---

# Audit: Prosocial Robot Navigation Charter

- **Card:** `src/prosoc/prnc/charter/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED with minor fixes — two should-fix items (a
  recurring Normative-Statement/description drift, and a stale
  `principles.md` cross-reference), no blocking issues.

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

### 2. `../_shared/principles.md`'s P9 summary row restates wording the charter itself deliberately trimmed — should-fix
- **Section/field:** `principles.md` P9 summary ("...without sacrificing own goals or task/context fit") vs. charter P9 Normative Statement / `description`
- **Issue:** The charter's 2026-08-19 EDITED entry (WI-CHARTER-FRONTIERS-SYNC)
  explicitly "trim[med] P9's task/context/goals qualifier (Section 2's
  definition retains it)" from P9's Normative Statement and YAML description.
  The shared `principles.md` reference table's P9 row still reads "Improve
  others' navigation experience, or preserve/improve shared navigability,
  without sacrificing own goals or task/context fit" — the pre-trim wording.
  Per `principles.md`'s own header, the charter is the sole source of truth
  and `principles.md` should be flagged as stale if the two disagree. They
  disagree here, specifically on a point the charter changed on purpose.
- **Recommended fix:** A human editor should update `principles.md`'s P9 row
  to match the charter's current, trimmed P9 wording (the qualifier remains
  true and findable via charter Section 2 and the P9 Explanation, just not in
  the Normative Statement/description any more). This audit does not edit
  `principles.md` itself, per this skill's scope.

### 3. P4 and P5 positive examples both illustrate "yielding to people passing" — suggestion
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
