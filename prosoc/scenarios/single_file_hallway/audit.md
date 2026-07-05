# Audit: Single File Hallway

- **Scenario:** `prosoc/scenarios/single_file_hallway/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Not ready — 3 blocking issues

## Findings

### 1. Duplicated `expected_behaviors.should_not` entries — blocking
- **Section/field:** `expected_behaviors.should_not` (embedded YAML in `scenario.md` and
  `scenario.yml`)
- **Issue:** The `should_not` list contains six entries, but only three distinct
  behaviors: "force the human to back up unexpectedly," "enter the hallway and create a
  stalemate," and "rely on last-moment braking to resolve the conflict" each appear
  twice, back to back. The embedded YAML block in `scenario.md` visibly shows the
  malformed source: a comment block reading "NOTE: Optional behaviors previously listed
  under `may` are intentionally subsumed under `should` to comply with the scenario
  schema..." is immediately followed by a second, duplicate copy of the same three
  `should_not` bullets rather than being merged into `should` as the comment claims. This
  is schema-valid (arrays have no uniqueness constraint and the dry-run distiller reports
  no diff/error) but is clearly unintentional duplication, not a deliberate authoring
  choice.
- **Recommended fix:** Remove the duplicate copy of the three `should_not` entries (and
  the now-stale comment about `may` being subsumed, since it inaccurately describes what
  happened — the content was duplicated into `should_not`, not merged into `should`) from
  both `scenario.md`'s embedded YAML and `scenario.yml`.

### 2. Missing "Scenario Card Summary" section — blocking
- **Section/field:** Scenario Card Summary (per `template.md`, "Required for AUDITED
  scenarios")
- **Issue:** `scenario.md` has no Scenario Card Summary section — it goes directly from
  the STATUS block to Overview, then straight into the YAML block. Fields such as
  Scenario Name, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role,
  Robot Task, Human Behavior, Ideal Outcome, Success/Quality Metrics, Related Scenarios,
  and Cited In are entirely absent from the prose, despite most being readily inferable
  from the YAML (which, unlike `robot_overtaking`, does already have a fairly complete
  `scenario_usage_guide` block to draw from).
- **Recommended fix:** Add a Scenario Card Summary section per `template.md`, populated
  from existing content, e.g. Scientific Purpose: proactivity / pedestrian interaction;
  Physical Environment: indoor; Geometric Layout: narrow single-file corridor; Robot
  Task: navigate hallway end-to-end; Human Behavior: approach from opposite end; Success
  Metrics: SR, NoCollisions, DeadlockFree; Related Scenarios: Frontal Approach, Movable
  Obstruction (both named explicitly in the Discussion section already).

### 3. Missing "Scenario Usage Guide" prose section — blocking
- **Section/field:** "Scenario Usage Guide" prose section (template.md, "Required for
  AUDITED scenarios")
- **Issue:** Unlike `robot_overtaking`, this scenario's YAML *does* contain a complete
  `scenario_usage_guide` block (success_metrics, quality_metrics, failure_modes,
  labeling_criteria all populated). However, `scenario.md` has no corresponding prose
  "Scenario Usage Guide" section with Success Metrics / Quality Metrics / Ideal Outcome /
  Failure Modes / Labeling Criteria subsections — the document jumps from the YAML block
  directly to "Discussion." Per the template, this is a required human-readable
  companion to the YAML, not merely optional restatement.
- **Recommended fix:** Add the "Scenario Usage Guide" section to `scenario.md`,
  transcribing the existing YAML content (success_metrics, quality_metrics,
  failure_modes, labeling_criteria) into prose form, plus an explicit Ideal Outcome
  statement (see Finding 4 below — there currently isn't one anywhere in the card).

### 4. No `ideal_outcome` field anywhere in the card — should-fix
- **Section/field:** `ideal_outcome` (schema.json top-level field; also required content
  per template.md's Scenario Card Summary and Scenario Usage Guide)
- **Issue:** Neither `scenario.md`'s embedded YAML nor `scenario.yml` sets
  `ideal_outcome`, and no prose section states one explicitly either. The closest
  available material is scattered across `evaluation_notes` ("preventing hesitation or
  discomfort") and the Overview's closing sentence ("prevent deadlock or discomfort"),
  but neither is phrased as a concise outcome statement.
- **Recommended fix:** Add `ideal_outcome`, e.g. "Robot and human recognize the
  single-file constraint early, one yields clearly, and both pass through the hallway
  without collision, backing up, or prolonged hesitation."

### 5. Reference to "Prosocial Behavior (P9)" — a principle outside P1–P8 — suggestion
- **Section/field:** Overview prose and `evaluation_notes`
- **Issue:** The prose repeatedly references "Prosocial Behavior (P9)" as a principle
  being deliberately excluded from this scenario's scope ("isolate and evaluate
  Proactivity (P7) without introducing opportunities for Prosocial Behavior (P9)"; "P9 is
  intentionally out of scope"). Per `_shared/principles.md`, the canonical principle set
  is only P1–P8; there is no P9. This does not appear in `relevant_principles` or
  `quality_metrics` (which correctly stay within P1–P8), so it is not a schema/charter
  compliance violation — it's confined to prose — but it references a principle ID that
  doesn't exist in the charter as documented here.
- **Recommended fix:** Either confirm P9 is a real, separately-tracked principle (e.g.
  from a newer charter revision not yet reflected in `_shared/principles.md`) and update
  the shared reference file accordingly, or rephrase the prose to avoid citing a
  numbered principle that isn't part of the canonical P1–P8 set — e.g. "without
  introducing opportunities for environmental stewardship or third-party benefit" (the
  Discussion section already uses this phrasing, which doesn't depend on a P9 label).

### 6. Minor over-specification phrasing — suggestion
- **Section/field:** `expected_behaviors.should` — "signal intent clearly (e.g., yielding
  or requesting priority)"
- **Issue:** This is phrased as a kind of behavior with illustrative examples in
  parentheses, which is consistent with P&G Guideline N6 (no exact motion or numeric
  threshold prescribed). Flagging only as a suggestion because the parenthetical could be
  read as narrowing the acceptable signaling mechanisms to those two; not a real
  violation.
- **Recommended fix:** No action required; optionally soften to "e.g., yielding,
  requesting priority, or other clear signaling" to keep the door open to other
  legible signaling strategies.

## Source Fidelity

SOURCE is explicitly cited as "Principles and Guidelines for Evaluating Social Robot
Navigation (P&G paper)" — a checkable source. However, per `_shared/pg_scenarios.md`,
"Single File Hallway" is **not** one of the 18 named entries in P&G Table 3. The
reference file's "Additional Scenarios (Figure 7, not in Table 3)" section states:

> The `single_file_hallway` scenario in the repo corresponds to the **Narrow Hallway**
> figure [in Figure 7]... If implementing these, note that they do not have full Table 3
> metadata and should be extrapolated carefully from the paper's descriptions and Figure
> 7.

Comparing the card against what's available:
- **Correspondence to Narrow Hallway (Figure 7):** The card's description — "a hallway
  that is too narrow for safe and comfortable passing... single-file passage" — is
  consistent with `pg_scenarios.md`'s one-line gloss: "single-file passage in a narrow
  corridor." No contradiction found against the limited data available.
- **No Table 3 metadata to compare against:** Because Narrow Hallway has no full Table 3
  entry (no Scientific Purpose, Robot Task, Human Behavior, Ideal Outcome fields listed
  in `pg_scenarios.md` beyond the one-line description), a field-by-field fidelity check
  like the one possible for Table 3 scenarios cannot be performed here.

**Source fidelity: partially checkable.** The high-level correspondence to the Figure 7
"Narrow Hallway" concept holds, but full fidelity (scientific purpose, geometric layout,
role assignments, ideal outcome) is **not checkable** against `pg_scenarios.md` beyond
that one-line gloss, per the reference file's own caveat that Figure-7-only scenarios
"do not have full Table 3 metadata." Verifying deeper fidelity would require reading the
P&G paper's Figure 7 discussion directly (not provided as `--paper` input for this
audit) — this audit does not fabricate that comparison.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Card Summary** (all subfields): **should probably be filled in now** — the
  section is entirely missing from prose, but nearly every field is directly inferable
  from the existing YAML and Discussion section (see Finding 2).
- **Scenario Usage Guide — Success Metrics:** present in YAML (`SR`, `NoCollisions`,
  `DeadlockFree`) but **should probably be filled in now** as a prose subsection per
  Finding 3 — the data exists, it just needs transcribing into `scenario.md`.
- **Scenario Usage Guide — Quality Metrics:** present in YAML (`P2`, `P3`, `P7`) — same
  as above, should probably be added as prose.
- **Scenario Usage Guide — Ideal Outcome:** **should probably be filled in now** — no
  `ideal_outcome` value exists anywhere in the card (YAML or prose); see Finding 4.
- **Scenario Usage Guide — Failure Modes:** present in YAML (three entries) — should
  probably be filled in now as prose per Finding 3.
- **Scenario Usage Guide — Labeling Criteria:** present in YAML (three entries) — should
  probably be filled in now as prose per Finding 3.
