---
name: prosoc-scenario-audit-all
description: >
  Audit the entire prosoc/scenarios/ corpus in one pass by fanning out
  prosoc-scenario-audit across every scenario, aggregating the results into a
  summary table and PR. Use this skill whenever the user asks to audit "all
  scenarios," "the whole corpus," "every scenario," or asks to re-run/refresh
  scenario audits repo-wide — as opposed to naming a single scenario, which is
  prosoc-scenario-audit's job. Branches off main, writes an audit.md per
  scenario plus a corpus-level AUDIT_SUMMARY.md, commits, and opens a PR.
---

# prosoc-scenario-audit-all Skill

This skill orchestrates `prosoc-scenario-audit` across every scenario under
`prosoc/scenarios/`, unmodified per-scenario, and aggregates the results. It does not
reimplement or fork any part of that skill's checklist — it dispatches to it and reads
its output contract.

Unlike `prosoc-scenario-audit`, this skill does take git actions on its own: it
branches, commits, and opens a PR, because a corpus-wide audit run is naturally a
single reviewable unit of work. It still never edits `scenario.md`, `scenario.yml`, or
any STATUS/STATE block, and it never promotes a scenario's lifecycle stage — those
remain human decisions, exactly as in `prosoc-scenario-audit`.

---

## Inputs

Optional:

- **A list of scenario names** — scope the run to a subset instead of the full corpus
  (e.g. re-auditing scenarios that were just edited). If omitted, the skill discovers
  every scenario dynamically (Step 2).
- **`--recurring-threshold <N>`** — minimum number of scenarios a finding must recur in
  to be called out as a repo-wide pattern (Step 6). Default: 3.

---

## Reference Knowledge

This skill does not duplicate `prosoc-scenario-audit`'s reference material. Each
dispatched subagent loads that skill's own reference set
(`../_shared/pg_scenarios.md`, `../_shared/principles.md`,
`../prosoc-scenario-audit/references/audit_checklist.md`, `schema.json`,
`workflow.md`, `template.md`) exactly as it would for a standalone invocation.

---

## Execution Steps

### 1. Branch off main

```bash
git checkout main
git pull
git checkout -b <branch-prefix>/audit-all-scenarios-<YYYY-MM-DD>
```

`<branch-prefix>` should follow whatever branch naming convention this repo already
uses (check recent branches with `git branch -r` or `git log --all --oneline` for the
pattern in use, e.g. `chore` or `<username>/chore`); it is not a fixed value. Use
today's date to avoid colliding with a still-open prior audit-all branch/PR. If
`main` has local uncommitted changes that would be clobbered, stop and report — do not
stash or discard anything without asking.

### 2. Enumerate scenarios

List subdirectories of `prosoc/scenarios/` that contain a `scenario.md` file. This
excludes non-scenario files at that level (`README.md`, `distill.py`, `schema.json`,
`template.md`, `workflow.md`).

If the user supplied an explicit scenario-name subset (Inputs), use that list instead
of the full discovery — but still validate each named directory contains a
`scenario.md`, and report (don't silently skip) any name that doesn't resolve.

### 3. Batch

Split the target scenario list into fixed batches of 2 (the last batch may have 1).
Each batch is dispatched to one subagent.

### 4. Fan out

For each batch, launch one subagent. Instruct it to run `prosoc-scenario-audit`'s exact
single-scenario procedure, unmodified, once per scenario in its batch — including that
skill's own frontmatter + prose output contract (see its SKILL.md Step 6). Always
overwrite any existing `audit.md` for a targeted scenario; this run is a fresh
point-in-time snapshot, not an incremental update.

Step 2 already guarantees every batched scenario has a `scenario.md`, so the only thing
that can still be missing at this stage is `scenario.yml`. If a scenario in a batch is
missing `scenario.yml`, that scenario is skipped (per `prosoc-scenario-audit`'s own stop
condition) — report it as skipped in the batch result, but do not fail the rest of the
batch over it.

### 5. Aggregate

Read every scenario's `audit.md` and parse its frontmatter (`scenario`, `verdict`,
`blocking`, `should_fix`, `suggestion`, `audited`). Build a summary table:

| Scenario | Verdict | Blocking | Should-fix | Suggestion |
|---|---|---|---|---|

Plus corpus totals (scenario count, count per verdict bucket, sum of each severity).

If an `audit.md` has no frontmatter (legacy format) or the frontmatter fails to parse,
do not silently drop it from the table — list it as a row with an explicit
"unparseable — needs re-audit" marker instead of a guessed verdict/counts.

### 6. Recurring patterns

Extract the canonical key for each finding from its `### N. <short title> — <severity>`
heading (see `prosoc-scenario-audit`'s SKILL.md Step 6 findings format): strip the
leading `N. ` numbering and the trailing ` — <severity>`, then case-fold the remaining
`<short title>`. Two findings recur under the same key only if their normalized titles
match exactly after this stripping — do not fuzzy-match on partial wording.

Group all findings across all scenarios by this key. Any key held by at least the
configured threshold (default 3, or `--recurring-threshold`) of *distinct scenarios*
(not distinct findings — a scenario contributes at most once per key) is a recurring
pattern. List these separately from the per-scenario findings, as observations noticed
while aggregating — not something any individual audit checked, since cross-scenario
consistency is explicitly out of scope for `prosoc-scenario-audit` itself. For each
recurring pattern, name the affected scenarios and suggest whether it looks like a
shared drafting-time error or a template/checklist gap worth fixing at the source
rather than scenario-by-scenario.

### 7. Write the corpus summary

Write `prosoc/scenarios/AUDIT_SUMMARY.md`, regenerating it wholesale (not appending):

```markdown
# Scenario Audit Summary

- **Run date:** <today's date>
- **Branch:** <branch name>
- **Scenarios audited:** <count> (<count skipped, if any>)

## Results

<Step 5's table>

**Totals:** <N> scenarios, <N> `ready`, <N> `ready_with_fixes`, <N> `not_ready`.
<N> blocking, <N> should-fix, <N> suggestion findings.

## Recurring Patterns

<Step 6's list, or "None found at threshold <N>.">
```

### 8. Commit

Stage every touched `audit.md` plus `AUDIT_SUMMARY.md` and commit. Do not stage
anything else — if `git status` shows unrelated changes, stop and ask rather than
sweeping them in.

### 9. Push and open the PR

Push the branch and open a PR whose body is the summary table plus recurring patterns
(same content as `AUDIT_SUMMARY.md`'s Results/Recurring Patterns sections), plus a test
plan confirming no `scenario.md`/`scenario.yml`/STATUS/STATE content was touched and no
scenario was promoted.

### 10. Report to the user

Tell the user:

- The branch name and PR URL
- Total scenarios audited (and any skipped)
- Verdict breakdown and total findings by severity
- The recurring patterns found (or that none met the threshold)

---

## Quality Checklist

Before reporting completion, verify:

- [ ] Every targeted scenario either has a freshly written `audit.md` or is reported
      as explicitly skipped (missing `scenario.yml`)
- [ ] No `scenario.md`, `scenario.yml`, `schema.json`, `template.md`, `distill.py`, or
      any STATUS/STATE block was modified anywhere in the corpus
- [ ] No scenario's lifecycle STATE was promoted
- [ ] `AUDIT_SUMMARY.md` was regenerated wholesale, not appended to
- [ ] The commit contains only `audit.md` files and `AUDIT_SUMMARY.md`
- [ ] The PR body's table matches `AUDIT_SUMMARY.md`

---

## What This Skill Does Not Do

- Does not reimplement, fork, or bypass `prosoc-scenario-audit`'s checklist — every
  per-scenario finding comes from an unmodified invocation of that skill
- Does not promote any scenario's STATE, or edit `scenario.md`/`scenario.yml`
- Does not treat a "not ready" or "unparseable" scenario as a reason to stop the run —
  the whole corpus is audited regardless of individual verdicts
- Does not merge or approve the PR it opens — that remains a human decision
