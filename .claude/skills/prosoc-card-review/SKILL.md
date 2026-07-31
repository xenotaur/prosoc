---
name: prosoc-card-review
description: >
  Human-in-the-loop review of a single prosoc normative card, one lifecycle
  step at a time — a scenario, task, context, constitution, the charter, or
  a packet manifest. Loads the card and its audit.md (running
  prosoc-card-audit first if missing or stale), adds an independent LLM
  recommendation and rationale beyond the audit's findings, and on
  explicit human confirmation calls prosoc-card-approve to perform the
  promotion. Use when a human wants a considered recommendation before
  deciding to promote a card, rather than promoting directly via
  prosoc-card-approve.
---

# prosoc-card-review Skill

This skill is the human-judgment layer between `prosoc-card-audit`
(machine-assisted findings) and `prosoc-card-approve` (mechanical
promotion). Given one card, it makes sure the card has current audit
evidence, forms an independent recommendation about the next lifecycle
step, presents both to a human, and — only on explicit approval — invokes
`prosoc-card-approve` to perform the promotion.

Like `prosoc-card-approve`, this skill handles exactly **one** lifecycle
step per invocation (`DRAFTED`/`EDITED` → `AUDITED`, or `AUDITED` →
`APPROVED`). Promoting a `DRAFTED` card all the way to `APPROVED` takes two
separate invocations of this skill — one per stage — each with its own
independent human decision, per `workflow.md`'s Design Principle 4
(authorship, review, and validation stay distinct stages, never conflated
into one action).

---

## Inputs

The user names a card — by id, directory name, or path — under one of the
six families, the same resolution `prosoc-card-audit` and
`prosoc-card-approve` use. An explicit family name may be given if the id
is ambiguous. "the charter" names the charter directly (no id).

If invoked by `prosoc-card-review-all`, the caller supplies the
`{family, id}` pair directly from the review queue — no resolution needed.

---

## Reference Knowledge

Load before reviewing:

1. **`prosoc/scenarios/workflow.md`** — lifecycle definitions, especially
   §4 (`AUDITED`) and §5 (`APPROVED`).
2. **`../_shared/principles.md`** — the P0–P9 principle definitions, needed
   to form an independent judgment about a card's charter alignment.
3. **`../_shared/audit_checklists/<family>.md`** — the same per-family
   rubric `prosoc-card-audit` uses, so this skill's recommendation is
   grounded in the same criteria the audit already checked, not a
   different or looser standard.

---

## Execution Steps

### 1. Locate and read the card

Use the same family/path resolution table as `prosoc-card-audit` (Step 1
of that skill). Read the card's Markdown and distilled YAML in full.

### 2. Ensure current audit evidence exists

Locate the card's `audit.md` (`prosoc/charter/audit.md` for the charter;
`prosoc/<family>/<id>/audit.md` otherwise).

**Staleness check:** if `audit.md` exists, compare the last commit
touching the card's Markdown/YAML against the last commit touching
`audit.md`:

```bash
git log -1 --format=%cI -- prosoc/<family>/<id>/<card-file>.md
git log -1 --format=%cI -- prosoc/<family>/<id>/audit.md
```

If the card file's last-commit timestamp is more recent than `audit.md`'s,
the audit is stale — the content it assessed has since changed.

**If `audit.md` is missing or stale:** invoke `prosoc-card-audit` for this
card now, without a separate confirm gate — it is non-destructive (writes
only a findings report, never touches the card) and is a necessary
precondition for this skill to proceed. Note in the final report that a
fresh audit was run and why.

**If `audit.md` exists and is current:** use it as-is.

### 3. Determine the target transition

Read the card's current `state:` (fenced YAML, authoritative). Apply
`prosoc-card-approve`'s Inputs rule: `DRAFTED`/`EDITED` → `AUDITED`, or
`AUDITED` → `APPROVED`. If the card is already `APPROVED` or later, or in
an end-of-life state (`DEPRECATED`/`RETIRED`), stop and report — there is
nothing to review toward promotion.

### 4. Form an independent recommendation

This is the step beyond what `prosoc-card-audit` already did. Read the
card's content directly (not just the audit's summary) against the
relevant checklist and `principles.md`, and form your own judgment:

- Do you agree with the audit's verdict and finding severities, or would
  you weigh anything differently?
- For a `→AUDITED` recommendation: is the audit's evidence (verdict
  `ready`/`ready_with_fixes`) actually sufficient grounds to advance, or
  do the should-fix findings collectively raise real doubt despite a
  passing verdict?
- For a `→APPROVED` recommendation: independent of the audit (which only
  speaks to machine-checkable coherence), does the card read as genuinely
  ready for a human to put their name behind — coherent, charter-aligned,
  fit for its stated use? Note anything the audit couldn't have caught
  (tone, framing, a subtly misleading normative statement).

State a clear recommendation — promote, or hold with a specific reason —
and the rationale behind it. Do not simply restate the audit's verdict
line; add genuine independent judgment, even when you end up agreeing with
it.

### 5. Confirm gate (human gate)

Present to the human:

- The card's family, id, current state, and target state
- The audit's verdict and finding counts (and whether it was freshly run
  this session)
- Your Step 4 recommendation and rationale
- Any should-fix/suggestion findings left unresolved (for `→APPROVED`
  specifically, remind the human these are being accepted as-is, not
  silently ignored)

Ask directly: promote, hold, or address findings first (offering
`prosoc-card-audit` — or, for a `→APPROVED` decision blocked by should-fix
findings, manual editing — as the alternative to promoting now).

**Wait for an explicit decision before proceeding.**

### 6. Act on the decision

- **Promote:** invoke `prosoc-card-approve` for this card and this exact
  transition. Per that skill's own Step 4, the confirmation just given
  here satisfies its confirm gate — do not ask the human to approve the
  same transition a second time.
- **Hold:** stop here. Record the reason in the report; do not touch the
  card.
- **Address findings first:** offer (do not auto-invoke) `prosoc-card-audit`
  for a fresh pass, or note the specific findings a human editor should
  address before the next review attempt.

### 7. Report

Tell the user:

- The transition performed, or the hold decision and its reason
- Whether a fresh audit was run this session (Step 2)
- The recommendation and rationale from Step 4
- If promoted: confirmation that `prosoc-card-approve` completed and
  `scripts/validate/status` reports the card consistent

---

## Quality Checklist

Before reporting completion, verify:

- [ ] Audit currency was checked (Step 2) via the git-timestamp comparison,
      not assumed
- [ ] A stale or missing audit triggered `prosoc-card-audit`, not a
      promotion against outdated findings
- [ ] The Step 4 recommendation is grounded in the card's actual content
      and the shared checklist/principles — not a restatement of the
      audit's verdict line alone
- [ ] The confirm gate (Step 5) was shown and an explicit decision
      received before any promotion was attempted
- [ ] Exactly one lifecycle step was in scope for this invocation
- [ ] `prosoc-card-approve` was not asked to re-confirm a transition this
      skill's own gate already approved

---

## What This Skill Does Not Do

- Does not perform the mechanical state edit itself — delegates to
  `prosoc-card-approve` once a human decides to promote.
- Does not re-implement `prosoc-card-audit`'s checklist logic — reuses the
  same shared checklists so its recommendation is grounded in the same
  criteria, not a parallel or looser standard.
- Does not promote more than one lifecycle step per invocation.
- Does not walk the corpus or determine review order — that is
  `prosoc-card-review-all`'s job, which calls this skill once per card in
  its ranked queue.
- Does not silently accept a stale audit — always checks currency first.
