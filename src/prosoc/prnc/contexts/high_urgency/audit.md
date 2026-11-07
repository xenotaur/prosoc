---
family: contexts
card: high_urgency
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 2
audited: 2026-11-07
---

# Audit: Emergency High-Urgency Operation

- **Card:** `src/prosoc/prnc/contexts/high_urgency/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Common tension wording drift — should-fix
- **Section/field:** Relationship to Prosocial Navigation Principles vs.
  `principle_emphasis.common_tensions`
- **Issue:** Prose lists "urgency versus perceived rudeness" as a common
  tension, but the YAML list has "urgency versus politeness" in that slot —
  a paraphrase, not the same phrase, and "perceived rudeness" and
  "politeness" aren't quite the same axis (one is an outcome/perception,
  the other a norm). Unresolved carryover from the 2026-07-29 audit; the
  2026-11-05/11-06 content edits did not touch this section.
- **Recommended fix:** Reconcile the wording — pick one phrasing and use it
  in both places (or note explicitly in prose if they are meant to describe
  slightly different things).

### 2. `related_contexts` prose/YAML mismatch — should-fix
- **Section/field:** Derived and Related Contexts vs. `related_contexts`
- **Issue:** Prose lists three related contexts (`service.routine_delivery`,
  `baseline.public_navigation`, `emergency.coordinated_response`), but the
  YAML `related_contexts` only has the first two. `emergency.coordinated_response`
  still has no matching card under `src/prosoc/prnc/contexts/` (confirmed: only
  `high_urgency`, `public_navigation`, and `routine_delivery` exist) — it remains
  a prose-only forward reference. Unresolved carryover from the 2026-07-29 audit.
- **Recommended fix:** Either add `emergency.coordinated_response` to
  `related_contexts` once it exists as a card (not before, per the "resolve
  to a real card" convention `related_scenarios` enforces for scenarios), or
  note explicitly in prose that it is a planned/future context rather than
  presenting it as an existing peer of the other two.

### 3. Task-axis one-sided wording — suggestion
- **Section/field:** Context Axes Instantiated → Task Context vs. `axes.task`
- **Issue:** Prose says "Delays are treated as significant failures" (no
  counterpart in the YAML), while the YAML adds "when safety constraints are
  respected" (no counterpart in the prose). Neither is a contradiction, but
  each is a one-sided addition — the YAML's safety-respecting caveat is a
  substantive qualifier (it's the same caveat the Normative Significance
  section states: "strong prioritization of task success when safety can be
  maintained") that would be worth echoing in the prose bullet too.
- **Recommended fix:** Fold the "when safety constraints are respected"
  caveat into the Task Context prose bullet, and/or fold "delays are treated
  as significant failures" into `axes.task`, so both sides carry the same
  content.

### 4. P9's two branches not distinguished in the deprioritization — suggestion
- **Section/field:** Relationship to Prosocial Navigation Principles vs.
  charter Principle 13 (P9) Explanation
- **Issue:** Not a contradiction, but a missed nuance. The charter's P9 has
  two branches: (a) actively improving another agent's navigation
  experience (discretionary, beyond-baseline, e.g. giving directions,
  holding a door), and (b) preserving or improving the shared environment's
  navigability (e.g. not leaving an obstruction behind, or clearing one
  that's already there) — charter §2 and Principle 13's Explanation. The
  card's "P9 is deprioritized" bullet treats P9 as a single undifferentiated
  concern. **Caught in review:** an earlier draft of this finding
  misattributed the charter's own urgency/delay example — "weigh [clearing
  an obstruction] against how much delay... and how urgent that task is" —
  to branch (a); the charter's own Explanation names clearing an obstruction
  as branch (b) explicitly. So the charter's chosen illustration for
  urgency-driven deprioritization is itself a branch (b) example, which
  argues *against*, not for, treating branch (b) as the one that "stays just
  as relevant under urgency." If anything, this is evidence the charter
  intends the deprioritization to cover both branches, or at least does not
  single out branch (a) as the only one affected — the opposite of this
  finding's original framing.
- **Recommended fix:** Optionally note in the P9 bullet that the charter's
  own illustrative example for P9-under-urgency is itself an environment-
  preservation (branch b) case, so the card's blanket "P9 is deprioritized"
  framing is, if anything, under-qualified in the other direction from what
  an earlier draft of this finding suggested. Not required for AUDITED —
  this is a refinement, not an error in the card.

## P9 Reclassification Coherence (this audit's focus)

The 2026-11-05 edit (PR #130) moved P9 from `emphasized` to `deprioritized`
in both prose and YAML, replacing a prior framing that conflated P9 with
P1 ("P9 ... interpreted as prioritizing harm prevention over everyday
politeness" — harm prevention is P1's role). This audit scrutinized whether
the new framing is independently correct, not merely internally consistent.

**Conclusion: the reclassification holds up.** It is well-grounded in the
charter's own Principle 13 (P9) Explanation, which is the canonical text
on how urgency should affect P9's exercise:

> "a delivery robot noticing an obstruction it could clear should weigh
> that against how much delay clearing it would add to its own task and
> how urgent that task is, not clear it unconditionally."

This is precisely the high-urgency case: the charter's own text ties
increased urgency to a *reduced* expectation that a robot will exercise
P9's discretionary acts, which directly supports "deprioritized" rather
than "emphasized." The card's prose — "the urgency that elevates P0 and
P1 leaves little slack for the discretionary, beyond-baseline acts P9
describes" — is an accurate paraphrase of that reasoning, not an
unsupported assertion.

The reclassification is also internally coherent against the context's
other principle-emphasis entries:
- **P0/P1 emphasized:** matches the charter's framing of goal achievement
  and safety as the principles urgency elevates (P8's canonical crash-cart
  illustration: "politeness is properly subordinate to task success").
- **P2/P3 deprioritized:** **caught in review -- corrected.** P8's
  crash-cart example explicitly names "politeness" yielding to task
  success, not comfort (P2) or legibility (P3) -- "politeness" is itself a
  distinct principle (P4) in this charter, not a synonym for P2/P3. P8's
  Explanation does state a *general* weighting rule (context determines
  the relative importance of every other principle), and extending that
  general rule to P2/P3 under high urgency is a reasonable inference, but
  it is an inference, not something the cited passage states explicitly --
  this paragraph should not have presented it as explicit canonical
  evidence. P9 (discretionary, "deliberately the lowest-severity
  principle") fits the deprioritization pattern more directly, on its own
  textual grounds -- P9's own `severity: optional` in `charter.yml` makes
  it the principle *most* disposed to being set aside under time pressure,
  independent of the P8/P2/P3 inference above.
- **P1 vs. P9 separation:** the new P1 bullet ("harm prevention is P1's
  role, not P9's") correctly draws the charter's own line — P1's Explanation
  is about not causing harm (a MUST-level, critical-severity constraint),
  while P9's Explanation is about discretionary, beyond-baseline helpfulness
  (an optional-severity concern). These are not substitutes for each other,
  and the card no longer implies they are.

The nuance between P9's two branches (noted as Finding 4 above, and
corrected there in review -- the charter's own urgency example is itself
a branch-(b) case, not a branch-(a) one) is a refinement opportunity, not
evidence that the reclassification itself is wrong. Nothing in the
charter's text about P9 contradicts treating it as deprioritized overall in
this context.

## Schema and Charter Compliance

- `scripts/distill/contexts --dry-run --show-diffs` produced no diff and no
  schema validation error for any context in the family, including
  `high_urgency` (whole-family dry-run; no other context showed drift
  either, so there is no out-of-scope aside to report).
- `principle_emphasis.emphasized` (P0, P1) and `.deprioritized` (P2, P3, P9)
  — all valid P0–P9 IDs, no overlap between the two lists.
- The deprioritized principles (P2, P3, P9) are all still actively discussed
  in prose with a stated rationale — annotated, not silently dropped, per
  Decision 6 of `PROP-NORMATIVE-PACKET-ASSEMBLY`.
- `axes.*` fields stay qualitative/descriptive throughout — no numeric
  weightings encoded, consistent with the template's explicit instruction.
- `related_contexts` entries (`service.routine_delivery`,
  `baseline.public_navigation`) both resolve to real context cards by their
  dotted `id` field. See Finding 2 for the third prose-only entry.
- `context.yml`'s top-level keys and nested objects (`axes.environmental`,
  `principle_emphasis`, `limits`) contain only the schema's allowed
  properties — no `additionalProperties` violations.
- `id`, `name`, `context_class`, `primary_robot_role`, and `applies_to_tasks`
  all match the Markdown's Context Summary and STATUS block.

## Completeness

All Required sections present: Context Summary, Context Description,
Normative Significance, Context Axes Instantiated (all five subsections),
Relationship to Prosocial Navigation Principles, Applicability and Limits.
Both optional-but-recommended sections (Derived and Related Contexts,
Example Scenario Classes) are populated — see Finding 2 for the one
content issue in the former.
