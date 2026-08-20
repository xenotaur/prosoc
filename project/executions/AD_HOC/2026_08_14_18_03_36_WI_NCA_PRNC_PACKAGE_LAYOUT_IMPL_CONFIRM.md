---
execution_id: 2026_08_14_18_03_36_WI_NCA_PRNC_PACKAGE_LAYOUT_IMPL_CONFIRM
prompt_id: PROMPT(AD_HOC:WI_NCA_PRNC_PACKAGE_LAYOUT_IMPL_CONFIRM)[2026-08-14T02:20:24+00:00]
work_item: AD_HOC
status: landed
rerun_of: 2026_08_14_01_21_24_WI_NCA_PRNC_PACKAGE_LAYOUT
pr: https://github.com/xenotaur/prosoc/pull/95
commit: a9ea0c35c59e4907a60d552b673add3147533533
created_at: 2026-08-14T18:03:36+00:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/95
session_transcript: claude-app:f087f2be-5992-4711-b12b-40cebb7e8305
---

# Summary

`/lrh-confirm-fixes` pre-merge verification pass for PR #95
(`WI-NCA-PRNC-PACKAGE-LAYOUT`), run as `/lrh-land`'s inlined Step 5.

**`rerun_of` note:** the mechanical target-verification algorithm
(`/lrh-land/references/land-workflow.md` § A separate, narrower
algorithm...) found no primary record — `UPPER_SLUG` derived from this
branch (`xenotaur/feat/wi-nca-prnc-package-layout-impl` →
`WI_NCA_PRNC_PACKAGE_LAYOUT_IMPL`) does not exactly match the primary
record's own slug (`WI_NCA_PRNC_PACKAGE_LAYOUT`, without `_IMPL`), because
that record was minted with `--slug wi-nca-prnc-package-layout` (matching
the WI ID) rather than the branch-derived slug the algorithm expects. Set
`rerun_of` manually to
`2026_08_14_01_21_24_WI_NCA_PRNC_PACKAGE_LAYOUT` — this session
authored that record directly and knows it is the genuine primary for
this PR — rather than leaving it empty per the algorithm's literal
"no match found" result, which would have been technically compliant
but factually wrong (this PR was created by `/lrh-implement`, not
outside it). Worth a future fix: either mint `/lrh-implement`'s primary
record slug from the branch name instead of the WI ID, or extend the
matching algorithm to also try the WI-ID-derived slug as a fallback.

# Result

Step 2 (gather state): `lrh github threads --mode raw --state all` on
PR #95 returned zero threads (`threads: []`) — no reviewer comments
exist yet, review or human. `lrh request review_response` independently
confirmed `Nothing to resolve:`. Both agree; no outdated-thread
discrepancy.

Provisional CI (Step 2.3) surfaced a real, genuine failure: `lint`
FAILING, `test`/`check-charter`/`check-packet-drift` PASSING.
`gh pr checks --required` errored ("no required checks reported");
distinguishing check (`gh api rules/branches/main`, 0
`required_status_checks` rules) confirmed this repo has no required-check
branch protection, so the unfiltered `gh pr checks` read is the correct
source. Root cause: `.github/workflows/lint.yml` still ran `ruff check
prosoc tests` / `black --check prosoc tests` against the pre-move flat
path — a real gap in `WI-NCA-PRNC-PACKAGE-LAYOUT`'s own implementation.
The work item's Required Changes step 6 only named `packet.yml`/
`charter.yml` explicitly; `lint.yml` (and `tests.yml`) exist in this
repo's `.github/workflows/` but were never enumerated or checked during
implementation.

Fixed `lint.yml`'s two `run:` lines to `ruff check src tests` / `black
--check src tests`, matching the equivalent local `scripts/lint`/
`scripts/format` fixes already made in the primary implementation.
Verified clean against the *exact* CI-pinned tool versions
(`ruff==0.16.3`, `black==25.12.0`, installed fresh) rather than trusting
local tool versions, which had earlier appeared to show ~22 pre-existing
formatting-drift files under a newer local black (26.5.1) — that drift
turned out to be purely a local-vs-CI version mismatch, not a real repo
issue: `black==25.12.0` (the pinned CI version) reports the full `src
tests` tree clean, 79 files unchanged.

While staging this fix, also found and cleaned up a self-inflicted
artifact from earlier in this session: the pre-push self-review pass
required a `git stash` / rebase-onto-updated-`main` / `git stash pop`
sequence (to pick up a doc file that had landed on `main` after this
branch started). Git's rename detection, applied to several
content-identical empty `__init__.py` files during that stash pop,
recreated four stray directories at the pre-move flat paths —
`tests/auditor/`, `tests/charter/`, `tests/literate/`, `tests/packet/` —
each containing only an orphaned `__init__.py` (plus stale `__pycache__`
directories from earlier local test runs), alongside the correct content
already present under `tests/nca/...`/`tests/prnc/...`. These were never
referenced by anything (confirmed: `scripts/test` passes identically
before and after removal, 259/259), so they were dead weight rather than
a functional bug, but they contradicted the work item's own acceptance
criterion that the moved tree contain no leftover pre-move paths. Removed
all four directories entirely (`git rm -r` for the tracked files, `rm -rf`
for the untracked `__pycache__`/empty-subdir debris) and amended them
into this round's commit before it was ever pushed, rather than adding a
separate cleanup commit.

Also confirmed, and explicitly did **not** fix as out of scope: `tests.yml`'s
`test: pass` is a pre-existing, unrelated false-green — its
`python -m unittest discover -v` invocation carries no `--pattern` flag,
so it uses the default `test*.py` glob, which never matches this repo's
actual `*_test.py`-suffixed test files, silently discovering and running
zero tests every time. Verified this predates this branch: the same "Ran
0 tests in 0.000s" appears on `main`'s current tip
(`76782eef332d10d45ed0bbdf01d15ee75a74d9c3`, checked via
`gh run view` on that commit's own `tests.yml` run) — not caused by this
PR, not a regression, and fixing it (a CI-behavior change unrelated to
the src/-layout migration) is out of this work item's scope. Flagging for
a separate follow-up.

Step 6 (thread-resolution verdict): **green** — zero threads existed, so
there is nothing to resolve and no exception left open.

Pushed the `lint.yml` fix as this round's `_CONFIRM` commit.

# Validation

- `lrh github threads --mode raw --state all` — `threads: []`
- `lrh request review_response` — `Nothing to resolve:`
- `gh pr checks --required` distinguishing check — 0
  `required_status_checks` rules on `main`; unfiltered read used
  correctly per that branch's documented fallback rule
- Provisional CI before the fix: `lint` FAILING (root-caused to
  `lint.yml`'s stale `prosoc`-path invocation), others passing
- `ruff==0.16.3 check src tests` — all checks passed (matches CI's
  pinned version exactly)
- `black==25.12.0 --check src tests` — 79 files unchanged (matches CI's
  pinned version exactly)
- `scripts/test` re-run after removing the four stray stash-pop
  directories — 259/259 tests, identical to before removal, confirming
  they were genuinely orphaned and not load-bearing for anything
- `lrh validate` — 0 errors, 0 warnings

## Step 8 — post-push re-checks and final verdict

**Environment disruption between pushes.** After the `lint.yml` fix above
was first pushed (as `e47dda7`), this session was interrupted for
approximately 5 real days (2026-08-14T18:06 → 2026-08-19T04:25 UTC per
`gh pr view`'s recorded push timestamp vs. the next live check) and the
local worktree checkout was lost entirely (`/Users/centaur/Workspace/
ProsocialRobotics/prosocial/...` no longer existed on disk). GitHub's
durable state was unaffected: PR #95 was still open at `e47dda7`, 3
commits, exactly as last pushed. CI had still not run on `e47dda7` after
those 5 days despite no GitHub incident, active (non-disabled) workflows,
and valid YAML — genuinely unexplained. Separately, `main` had advanced 2
commits (PR #92) in the interim, which — coincidentally — also created
`project/sessions/index.jsonl` as a first-writer, the same file this PR's
own `record-session-alias` call created, producing a real `add/add`
conflict (`mergeable: CONFLICTING`) once main moved. Nothing else PR #92
touched overlapped this PR's files.

Recovered by creating a fresh worktree from the still-intact primary
checkout, rebasing onto `origin/main` (one conflict, in
`project/sessions/index.jsonl`: resolved as a union of both PRs'
independent JSONL entries — no semantic conflict, both are legitimate
```append-only``` log lines), re-running the full validation suite against
the rebased tree (`lrh validate`, `scripts/test` 259/259 with `openai`/
`python-dotenv` installed matching the earlier-documented pre-existing
gap, `ruff==0.16.3`/`black==25.12.0` exact-pinned-version check, wheel
build, `scripts/assemble --check` against the golden packet,
`papers/01_charter/render.py` byte-identical to its golden `.tex`), and
pushing with `--force-with-lease` (new HEAD `dcbf297`, since the rebase
rewrote the branch's commit SHAs). `mergeable` flipped to `MERGEABLE`
immediately after the push. This round's `commit:` field above reflects
this final, force-pushed SHA.

**CI on `dcbf297`:** this time triggered promptly (within ~1 minute of
the force-push, unlike the mysterious 5-day silence on the prior SHA) —
all 4 checks (`lint`, `test`, `check-charter`, `check-packet-drift`)
reported `SUCCESS`.

**REVIEW-LANDED check on `dcbf297`:** `gh api .../pulls/95/reviews`
returned exactly one formal review — Copilot's automatic first-push pass,
`commit_id: 011ebb9...` (this PR's *first* commit, three commits and one
rebase behind current HEAD) reporting no comments. Per the `commit_id`
must-match-current-`HEAD` rule, this does not cover `dcbf297`. Zero
review threads exist (`reviewThreads` GraphQL query: empty). No automatic
reviewer response covers the current HEAD, and only ~4 minutes had
elapsed since the force-push (Copilot's auto-trigger is tied to PR-open/
first-push, not to every subsequent force-push, so waiting longer was not
expected to produce one). Per the no-manual-bot-retrigger policy,
dispatched a substitute `/lrh-self-review` PR-mode pass (cold-context
`general-purpose` subagent, given only the PR URL and current HEAD SHA) —
it cloned the branch independently, ran the full validation suite itself
(all confirmed passing, including a from-scratch content-hash comparison
of all 161 pre-move files against their new locations), and reported two
non-blocking findings, both **Problematic comment**-bucket (real
observations that conflict with this work item's own documented scope,
not defects in the restructuring): (1) several `.claude/skills/*/
SKILL.md` and `_shared/*.md` files (not the 6 `_shared/audit_checklists/
*.md` files this work item's Required Changes step 6 explicitly named)
still reference pre-move flat paths — already known and deliberately
left out of scope by this PR's own primary execution record; (2)
`.github/workflows/tests.yml` silently runs zero tests
(`unittest discover` default pattern doesn't match this repo's
`*_test.py`-suffixed files) — already independently confirmed pre-existing
and unrelated to this migration during this same confirm-fixes pass
(see the `tests.yml` note above). Verdict: **safe to merge as-is**.

Independently re-verified (mandatory Step 4) the top finding directly
rather than accepting it at face value: read
`.claude/skills/prosoc-card-audit/SKILL.md` and confirmed it does contain
multiple stale `prosoc/scenarios`/`prosoc/charter` references, and ran
`git diff aaae08b dcbf297 -- .claude/skills/prosoc-card-audit/SKILL.md`
(empty output) confirming the file is genuinely untouched by this PR — the
subagent's claim holds exactly as reported.

**Final verdict: GREEN.** Thread-resolution verdict green (0 threads),
CI green on `dcbf297` (4/4 checks), REVIEW-LANDED satisfied via the
substitute self-review pass (no blocking findings; both surfaced findings
are Problematic-comment/skip-rationale, already documented as
out-of-scope). Merge command:

```bash
gh pr merge https://github.com/xenotaur/prosoc/pull/95 --match-head-commit dcbf297c2e0576bc60f2be89b23b71abad7e1b3f <merge-mode-flag>
```

Merge-mode flag left unresolved in this record — this repo's recent PR
history mixes `--merge` (2-parent commits, e.g. PR #89, #91) and
`--squash` (1-parent, `(#N)`-suffixed titles, e.g. PR #90, #92, #93) with
no clear single standard; asked the human at the Step 6 merge gate rather
than guessing.

# Follow-up

- Separately worth filing (not blocking this PR): `tests.yml`'s
  `python -m unittest discover -v` has silently run zero tests for at
  least as long as `main`'s current tip predates this branch — a
  standing, masked CI gap unrelated to this migration. Independently
  confirmed twice now (once by this session directly, once by the
  substitute self-review subagent).
- Separately worth filing (not blocking this PR): several `.claude/
  skills/*/SKILL.md` and `_shared/*.md` files (enumerated by the
  substitute self-review subagent's report) still reference pre-move
  flat `prosoc/...` paths — out of this work item's explicit Required
  Changes scope (only the 6 `_shared/audit_checklists/*.md` files were
  named), but worth a follow-up cleanup since these are live,
  actively-used skill instructions.
- Slug-derivation mismatch noted above (see `rerun_of` note) — worth a
  small process fix so future `rerun_of` lookups don't need manual
  override.
- Worth a standing process note: the 5-day CI silence on `e47dda7` (zero
  workflow runs, no GitHub incident, valid YAML, active workflows) was
  never root-caused — it's possible GitHub simply stops queuing new
  `pull_request: synchronize` runs against a commit once the PR sits in
  a stale/conflicting-with-base state for long enough, and the
  force-push (which also resolved the conflict) is what actually
  unstuck it, but this is speculative; if it recurs, worth escalating to
  GitHub support with this PR as a reference case.
