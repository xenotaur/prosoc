---
name: prosoc-card-audit-all
description: >
  Audit an entire prosoc card family (or several families, or the whole
  corpus) in one pass by fanning out prosoc-card-audit across every card,
  aggregating the results into a summary table and PR. Use this skill
  whenever the user asks to audit "all scenarios," "all tasks," "every
  context," "the whole corpus," or asks to re-run/refresh audits repo-wide —
  as opposed to naming a single card, which is prosoc-card-audit's job.
  Branches off main, writes an audit.md per card plus AUDIT_SUMMARY.md
  file(s), commits, and opens a PR. Family-dispatched successor to
  prosoc-scenario-audit-all.
---

# prosoc-card-audit-all Skill

This skill orchestrates `prosoc-card-audit` across every card in one family,
several families, or the whole corpus, unmodified per-card, and aggregates the
results. It does not reimplement or fork any part of that skill's checklists —
it dispatches to it and reads its output contract.

Unlike `prosoc-card-audit`, this skill does take git actions on its own: it
branches, commits, and opens a PR, because a multi-card audit run is naturally
a single reviewable unit of work. It still never edits any card's Markdown,
YAML, or STATUS/STATE block, and it never promotes a card's lifecycle stage —
those remain human decisions, exactly as in `prosoc-card-audit`.

This skill supersedes the retired `prosoc-scenario-audit-all` (its exact
orchestration logic is preserved here, generalized to six families rather
than scenarios only, per `PROP-NORMATIVE-PACKET-ASSEMBLY` Decision 7 and its
Phase 2 manifest-family extension).

---

## Inputs

Optional:

- **One or more family names** (`scenarios`, `tasks`, `contexts`,
  `constitutions`, `charter`, `manifests`). If omitted, run across all six.
- **A list of card names**, scoped to a single named family — to audit a
  subset instead of that family's full corpus (e.g. re-auditing cards that
  were just edited). Only valid when exactly one family is given; a card-name
  subset with multiple/omitted families is ambiguous — ask the user to narrow
  to one family first.
- **`--recurring-threshold <N>`** — minimum number of distinct cards a finding
  must recur in to be called out as a pattern (Step 6). Default: 3.

---

## Reference Knowledge

This skill does not duplicate `prosoc-card-audit`'s reference material. Each
dispatched subagent loads that skill's own reference set — the resolved
family's checklist under `../_shared/audit_checklists/`, `../_shared/
principles.md`, `../_shared/pg_scenarios.md` (scenarios only), each family's
`schema.json`, `workflow.md`, `template.md` — exactly as it would for a
standalone invocation.

---

## Execution Steps

### 1. Branch off main

```bash
git checkout main
git pull
git checkout -b <branch-prefix>/audit-all-cards-<YYYY-MM-DD>
```

`<branch-prefix>` should follow whatever branch naming convention this repo
already uses (check recent branches with `git branch -r` or `git log --all
--oneline`; it is not a fixed value). Use today's date to avoid colliding with
a still-open prior audit-all branch/PR. If `main` has local uncommitted
changes that would be clobbered, stop and report — do not stash or discard
anything without asking.

### 2. Enumerate cards

For each target family:

| Family | Enumeration |
|---|---|
| scenarios | subdirectories of `src/prosoc/prnc/scenarios/` containing a `scenario.md` |
| tasks | subdirectories of `src/prosoc/prnc/tasks/` containing a `task.md` |
| contexts | subdirectories of `src/prosoc/prnc/contexts/` containing a `context.md` |
| constitutions | subdirectories of `src/prosoc/constitutions/` containing a `constitution.md` |
| charter | exactly one card: `{family: charter, id: "charter"}` — no directory enumeration |
| manifests | subdirectories of `src/prosoc/manifests/` containing a `manifest.md` |

This excludes non-card files at each family's top level (`README.md`,
`distill.py`, `schema.json`, `template.md`, `AUDIT_SUMMARY.md`,
`workflow.md` for scenarios).

If the user supplied an explicit card-name subset (Inputs, single-family
only), use that list instead of full discovery for that family — but still
validate each named directory contains the expected Markdown file, and report
(don't silently skip) any name that doesn't resolve.

### 3. Batch

Across all targeted `{family, id}` pairs, split into fixed batches of 2 (the
last batch may have 1). Each batch is dispatched to one subagent — batches may
mix families.

### 4. Fan out

For each batch, launch one subagent. Instruct it to run `prosoc-card-audit`'s
exact single-card procedure, unmodified, once per `{family, id}` pair in its
batch — including that skill's own frontmatter + prose output contract (see
its SKILL.md Step 6). Always overwrite any existing `audit.md` for a targeted
card; this run is a fresh point-in-time snapshot, not an incremental update.

Step 2 already guarantees every batched card has its Markdown file, so the
only thing that can still be missing at this stage is the distilled YAML
(`scenario.yml`, `task.yml`, `context.yml`, `constitution.yml`, or
`charter.yml`, per family). If a card in a batch is missing it, that card is
skipped (per
`prosoc-card-audit`'s own stop condition) — report it as skipped in the batch
result, but do not fail the rest of the batch over it.

### 5. Aggregate

Read every audited card's `audit.md` and parse its frontmatter (`family`,
`card`, `verdict`, `blocking`, `should_fix`, `suggestion`, `audited`). Build a
summary table:

| Family | Card | Verdict | Blocking | Should-fix | Suggestion |
|---|---|---|---|---|---|

Plus totals per family and corpus-wide (card count, count per verdict bucket,
sum of each severity).

If an `audit.md` has no frontmatter (legacy format) or the frontmatter fails
to parse, do not silently drop it from the table — list it as a row with an
explicit "unparseable — needs re-audit" marker instead of a guessed
verdict/counts.

### 6. Recurring patterns

Extract the canonical key for each finding from its `### N. <short title> —
<severity>` heading (see `prosoc-card-audit`'s SKILL.md Step 6 findings
format): strip the leading `N. ` numbering and the trailing ` — <severity>`,
then case-fold the remaining `<short title>`. Two findings recur under the
same key only if their normalized titles match exactly after this stripping —
do not fuzzy-match on partial wording.

Group all findings across all audited cards in this run by this key,
regardless of family. Any key held by at least the configured threshold
(default 3, or `--recurring-threshold`) of *distinct cards* (not distinct
findings — a card contributes at most once per key) is a recurring pattern.
List these separately from the per-card findings, as observations noticed
while aggregating — not something any individual audit checked, since
cross-card consistency is explicitly out of scope for `prosoc-card-audit`
itself. For each recurring pattern, name the affected family/card pairs and
suggest whether it looks like a shared drafting-time error or a
template/checklist gap worth fixing at the source rather than card-by-card. A
pattern spanning multiple families is worth calling out explicitly — it more
strongly suggests a shared checklist or template gap than a per-family one.

### 7. Write the summary file(s)

Per the workstream's settled convention:

- **A run scoped to exactly one family** writes that family's
  `prosoc/<family>/AUDIT_SUMMARY.md`, regenerated wholesale (not appended).
- **A run spanning multiple families or the whole corpus** writes one
  aggregate to `project/audits/CARD_AUDIT_SUMMARY.md` covering every family
  touched, **and** regenerates each touched family's own
  `prosoc/<family>/AUDIT_SUMMARY.md` scoped to just that family's cards.

Template (adapt the header for a single-family vs. multi-family run):

```markdown
# Card Audit Summary

- **Run date:** <today's date>
- **Branch:** <branch name>
- **Scope:** <family name, or "all six families", or a listed subset>
- **Cards audited:** <count> (<count skipped, if any>)

## Results

<Step 5's table>

**Totals:** <N> cards, <N> `ready`, <N> `ready_with_fixes`, <N> `not_ready`.
<N> blocking, <N> should-fix, <N> suggestion findings.

## Recurring Patterns

<Step 6's list, or "None found at threshold <N>.">
```

### 8. Commit

Stage every touched `audit.md` plus the summary file(s) from Step 7. Do not
stage anything else — if `git status` shows unrelated changes, stop and ask
rather than sweeping them in.

### 9. Push and open the PR

Push the branch and open a PR whose body is the summary table plus recurring
patterns (same content as the summary file's Results/Recurring Patterns
sections), plus a test plan confirming no card Markdown/YAML/STATUS/STATE
content was touched and no card was promoted.

### 10. Report to the user

Tell the user:

- The branch name and PR URL
- Total cards audited (and any skipped), broken down by family
- Verdict breakdown and total findings by severity
- The recurring patterns found (or that none met the threshold)

---

## Quality Checklist

Before reporting completion, verify:

- [ ] Every targeted card either has a freshly written `audit.md` or is
      reported as explicitly skipped (missing its distilled YAML)
- [ ] No card's Markdown, YAML, `schema.json`, `template.md`, `distill.py`, or
      any STATUS/STATE block was modified anywhere in the audited scope
- [ ] No card's lifecycle STATE was promoted
- [ ] Summary file(s) were regenerated wholesale, not appended to, at the
      correct path(s) per Step 7's single-family vs. multi-family rule
- [ ] The commit contains only `audit.md` files and the summary file(s)
- [ ] The PR body's table matches the summary file(s)

---

## What This Skill Does Not Do

- Does not reimplement, fork, or bypass `prosoc-card-audit`'s checklists —
  every per-card finding comes from an unmodified invocation of that skill
- Does not promote any card's STATE, or edit any card's Markdown/YAML
- Does not treat a "not ready" or "unparseable" card as a reason to stop the
  run — every targeted card is audited regardless of individual verdicts
- Does not merge or approve the PR it opens — that remains a human decision
