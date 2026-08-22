---
name: prosoc-card-approve
description: >
  Promote a single prosoc normative card's lifecycle state one step forward
  — from DRAFTED/EDITED to AUDITED, or from AUDITED to APPROVED — a
  scenario, task, context, constitution, the charter, or a packet manifest.
  Mechanical, confirm-gated primitive: edits the fenced-YAML state: field,
  regenerates the card's distilled YAML via its family's distiller, and
  projects the change into the Markdown STATUS block via
  scripts/validate/status --fix. Never edits normative content. Use when a
  card already has the evidence its next lifecycle step requires and a
  human is ready to promote it directly, without the recommendation/
  rationale layer prosoc-card-review adds.
---

# prosoc-card-approve Skill

This skill performs the mechanical half of promoting a prosoc normative
card's lifecycle state one step, per `src/prosoc/prnc/scenarios/workflow.md` and
`PROP-NORMATIVE-CARD-APPROVAL` Decision 2. It is a state-transition
primitive: it edits exactly the `state:` field (plus the files a state
change requires to stay consistent), asks for explicit human confirmation
before writing anything, and never touches a card's normative content.

Two transitions are supported, each with its own evidence gate:

- **`→AUDITED`** (from `DRAFTED` or `EDITED`): requires an `audit.md` next
  to the card with `verdict: ready` or `verdict: ready_with_fixes`. This
  evidence is machine-generated (by `prosoc-card-audit`), so this
  transition needs no additional human judgment beyond accepting that the
  audit exists and passed.
- **`→APPROVED`** (from `AUDITED`): requires the card's current state
  already be `AUDITED`. No additional evidence is required beyond that —
  approval is a human accountability attestation (workflow.md's Design
  Principle 3), not a second content review. The human confirming at Step
  4 below *is* the evidence for this transition.

No other transition is in scope. This skill never promotes more than one
step in a single invocation (no `DRAFTED`→`APPROVED` skip), never demotes,
and never touches `VALIDATED`/`DEPRECATED`/`RETIRED`.

---

## Inputs

The user names a card — by id, directory name, or path — under one of the
six families, the same resolution `prosoc-card-audit` uses:

- **An explicit family name** (`scenarios`, `tasks`, `contexts`,
  `constitutions`, `charter`, `manifests`), if the card id alone is
  ambiguous.
- **`--to AUDITED|APPROVED`** (optional) — the target state. If omitted,
  the target is the card's current state's next step in the chain
  (`DRAFTED`/`EDITED` → `AUDITED`; `AUDITED` → `APPROVED`). If the card is
  already at or past the requested target, or the requested target skips a
  step, stop and report rather than guessing what the user meant.
- **"the charter"** — the charter has no per-card id; naming it directly is
  sufficient.

If the family isn't stated, resolve it the same way `prosoc-card-audit`
does: check which family directory the named id resolves under
(`src/prosoc/prnc/scenarios/<id>/`, `src/prosoc/prnc/tasks/<id>/`,
`src/prosoc/prnc/contexts/<id>/`, `src/prosoc/constitutions/<id>/`,
`src/prosoc/manifests/<id>/`, in that order). If
ambiguous or unresolvable, ask the user to state the family explicitly.

---

## Reference Knowledge

Load these before promoting:

1. **`src/prosoc/prnc/scenarios/workflow.md`** — the lifecycle definition and the
   evidence-gate rationale for each stage (§4 `AUDITED`, §5 `APPROVED`).
2. **`src/prosoc/prnc/<family>/schema.json`** (or `src/prosoc/<family>/schema.json`
   for constitutions/manifests) — the JSON schema the card's distilled
   YAML must conform to (used only to confirm the target `state` value is
   schema-valid before writing it; this skill does not re-run a full
   schema validation pass).

---

## Execution Steps

### 1. Locate and read the card

| Family | Card path | Card YAML | Distiller (regenerate, not `--dry-run`) |
|---|---|---|---|
| scenarios | `src/prosoc/prnc/scenarios/<id>/scenario.md` | `scenario.yml` | `scripts/distill/scenarios --scenario <id>` |
| tasks | `src/prosoc/prnc/tasks/<id>/task.md` | `task.yml` | `scripts/distill/tasks` (whole family, no per-card scoping) |
| contexts | `src/prosoc/prnc/contexts/<id>/context.md` | `context.yml` | `scripts/distill/contexts` (whole family) |
| constitutions | `src/prosoc/constitutions/<id>/constitution.md` | `constitution.yml` | `scripts/distill/constitutions` (whole family) |
| charter | `src/prosoc/prnc/charter/charter.md` | `charter.yml` (no id) | `scripts/distill/charter` |
| manifests | `src/prosoc/manifests/<id>/manifest.md` | `manifest.yml` | `scripts/distill/manifests` (whole family) |

If either file is missing, stop and report — do not proceed.

Read the card's embedded fenced YAML to find the current `state:` field
(for constitutions, it is nested under the `constitution:` root key; for
every other family it is top-level). This — not the Markdown `STATE` line
— is the authoritative source per `PROP-NORMATIVE-PACKET-ASSEMBLY`
Decision 2; the Markdown line is a projection of it.

### 2. Determine the target transition

Apply the Inputs section's rule to fix `<from>` → `<to>`. If the resolved
transition is not one of `DRAFTED|EDITED → AUDITED` or `AUDITED →
APPROVED`, stop and report why (e.g. "card is already `APPROVED`", "cannot
skip `AUDITED`").

### 3. Evidence gate

**For `→AUDITED`:** locate `audit.md` next to the card (`src/prosoc/prnc/charter/audit.md`
for the charter; `src/prosoc/prnc/<family>/<id>/audit.md` for scenarios/tasks/contexts,
or `src/prosoc/<family>/<id>/audit.md` for constitutions/manifests). If it does not
exist, stop and report — recommend running `prosoc-card-audit` first. If it
exists, read its frontmatter `verdict:` field. If `not_ready`, stop and
report the blocking findings — do not promote. If `ready` or
`ready_with_fixes`, the gate passes.

**For `→APPROVED`:** confirmed by Step 1's read (`state: AUDITED`). No
further evidence check.

### 4. Confirm gate (human gate)

Before touching any file, show the user:

- The card's family, id, and current state
- The target state
- For `→AUDITED`: the audit's one-line verdict and finding counts
  (blocking/should-fix/suggestion) from `audit.md`'s frontmatter
- For `→APPROVED`: a reminder that this is a human accountability
  attestation — the user should have read the card and its `audit.md`
  before confirming, not just this summary

**Wait for explicit confirmation before writing anything.** A vague or
implied approval is not sufficient — require an unambiguous yes. If a
calling skill (`prosoc-card-review`) already showed this exact transition
at its own confirm gate and received explicit approval earlier in the same
session, that approval satisfies this gate too — do not re-ask. A
standalone invocation always shows this gate itself.

### 5. Execute the promotion

In order:

1. Edit the card's embedded fenced YAML `state:` field (via the Edit tool)
   from `<from>` to `<to>`. Do not touch any other field.
2. Regenerate the card's distilled YAML by running that family's
   distiller (Step 1's table) **without** `--dry-run`. Confirm the
   distiller reports success and the regenerated `.yml`'s `state` field
   now matches `<to>`.
3. Project the new state into the Markdown `STATUS`/`Status` block:

   ```bash
   scripts/validate/status --fix --family <family> --card <id>
   ```

   (charter has no `--card`; omit it and rely on `--family charter` alone,
   consistent with its single-source, `label_by_stem` registration.)
4. Re-verify consistency (no `--fix`):

   ```bash
   scripts/validate/status --family <family> --card <id>
   ```

   Must report `ok`. If it does not, stop and report — do not leave the
   card in a partially-promoted state without telling the user.

### 6. Report

Tell the user:

- The transition performed (`<from>` → `<to>`)
- Confirmation that `scripts/validate/status` now reports the card
  consistent
- A reminder that no normative content was touched — only the `state:`
  field and its two projections (distilled YAML, Markdown `STATUS` line)

---

## Quality Checklist

Before reporting completion, verify:

- [ ] Exactly one transition was performed (`→AUDITED` or `→APPROVED`),
      never a multi-step skip
- [ ] The evidence gate for the performed transition was checked and
      passed before any file was touched
- [ ] The confirm gate (Step 4) was shown and explicit approval received
      before any file was touched
- [ ] Only the `state:` field (and its Markdown-line projection) changed —
      no other line in the card's Markdown or YAML was modified
- [ ] The family's distiller was re-run (not `--dry-run`) so the
      distilled `.yml` reflects the new state
- [ ] `scripts/validate/status --family <family> --card <id>` reports `ok`
      after the promotion, with no `--fix` needed

---

## What This Skill Does Not Do

- Does not edit any card's normative content — only its `state:` field and
  that field's Markdown projection.
- Does not perform a content review or produce audit findings — that is
  `prosoc-card-audit`'s job; this skill only checks that `audit.md`
  already exists with a passing verdict.
- Does not add LLM recommendation or rationale beyond the mechanical
  evidence-gate check — that layer is `prosoc-card-review`'s job, which
  calls this skill once a human has decided to promote.
- Does not walk the corpus or rank cards by priority — that is
  `prosoc-card-review-all`'s job.
- Does not skip lifecycle stages, demote a card, or touch
  `VALIDATED`/`DEPRECATED`/`RETIRED`.
- Does not require a second confirmation when a caller (`prosoc-card-review`)
  has already shown the same transition at its own confirm gate and
  received explicit approval in the same session — that approval satisfies
  Step 4 here too. Standalone invocation still always shows Step 4 itself.
