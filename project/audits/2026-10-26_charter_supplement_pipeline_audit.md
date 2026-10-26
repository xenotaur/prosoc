# Charter supplement pipeline audit: handoff-claim verification

An external handoff prompt (not authored in this repo) claimed 13 defect
categories in the `papers/01_charter` Frontiers supplementary-material
pipeline — source cards, renderer, template, tests, and CI — and asked for
them to be fixed. Before any repo changes were made, two independent
read-only sessions checked every claim against the actual tree: exact file
paths, line numbers, git history, and execution records, not just
plausibility. This document is the resulting evidence record. It does not
implement any fix; see the workstream/work items it feeds for that.

**Run dates:** 2026-10-25 (first pass) and 2026-10-26 (second-opinion
pass, corrections folded in here). **Scope:** `papers/01_charter/**`, the 9
sources in `papers/01_charter/sources.txt`, `src/prosoc/nca/utils/papers/render.py`,
`papers/01_charter/template.tex`, `tests/nca/utils/papers/render_test.py`,
`.github/workflows/charter.yml`, `papers/01_charter/README.md`.

## Headline correction: the charter's `APPROVED` state is legitimate

The original handoff's most consequential claim was that the charter's
lifecycle metadata is contradictory enough that `state: APPROVED` might be
unjustified, and suggested the pipeline should refuse to publish an
unaudited `APPROVED` charter. **Acting on that claim literally would be a
mistake.** The charter's `state: APPROVED` (`src/prosoc/prnc/charter/charter.yml`)
is earned, not stale:

- PR #79 contains a commit titled *"Promote charter EDITED -> AUDITED ->
  APPROVED; regenerate sample_packet golden."*
- PR #97's execution record
  (`project/executions/WI-CHARTER-FRONTIERS-SYNC/2026_08_19_22_19_50_WI_CHARTER_FRONTIERS_SYNC.md:20-39`)
  states the charter was "re-audited, and carried ... back through EDITED →
  AUDITED → APPROVED" via `prosoc-card-approve`, run twice.
- `src/prosoc/prnc/charter/audit.md` is dated 2026-08-19 — the same day as
  that promotion — verdict `ready`, 0 blocking, 0 should-fix.

What's actually wrong is display/bookkeeping only:
1. `charter.md:4`'s free-text `**Status:** Draft (Normative)` header is
   stale and contradicts the authoritative `## Status` block and embedded
   YAML a few lines below it.
2. The edit-history bullets record two "reverted from APPROVED pending
   re-audit" entries but no matching "re-approved on \<date\>" entry closing
   either loop.

**No work item arising from this audit should change any card's `state:`
field.** The fix is the stale header line and the missing history bullet,
plus a validator change described below.

## Confirmed as originally claimed

Checked exactly against the current tree, no corrections needed:

- **Collapsed lists at the cited locations** — `\textbf{Includes:} -`
  /`\textbf{Excludes:} -` run-on prose at `golden/rendered.tex` lines
  ~1814, 1819, 2014, 2019, 2325, 2329, 2619, 2622, 2908, 2912, caused by a
  missing blank line between a bold label and a Markdown list in the
  source cards.
- **Double-numbered headings** — `## 1. Purpose of This Charter` (and
  `2.` through at least `14.`) in `charter.md` render as
  `\subsection{1. Purpose of This Charter}`, which the Frontiers class will
  then number again.
- **No `literate=` Unicode mapping** — the `literatecard` `lstlisting`
  style in `papers/01_charter/template.tex:53-60` has no character
  mappings, and the en dash / em dash characters that trigger the known
  corruption sit inside `\begin{lstlisting}[style=literatecard]` blocks
  (confirmed by location; PDF compilation wasn't available in either
  session's sandbox to confirm the actual glyph loss — see below).
- **Bare citation numbers** — `frontal_approach/scenario.md:29`'s
  `**Cited In:** 50, 126, 167` has no bibliography machinery resolving it
  in the standalone supplement template.
- **No PDF build entry point** — `render.py`'s `main()` explicitly rejects
  any arguments ("this renderer takes no arguments"); there is no
  `--pdf`/`--check` path, no `pdflatex` invocation, no `pdftotext` check
  anywhere in the pipeline.
- **CI doesn't exercise the supplement** — `.github/workflows/charter.yml`
  only runs `scripts/distill/charter --dry-run` and a `charter.yml` diff
  check; its `paths:` trigger doesn't include `papers/**`, and nothing
  renders or compiles anything.
- **Stale README** — `papers/01_charter/README.md:37` says the shim
  delegates to `prosoc.utils.papers.render`; the code
  (`papers/01_charter/render.py:17`) imports `prosoc.nca.utils.papers.render`.

## Confirmed but corrected or widened

- **Lifecycle validator (task/context cards).** The 5 cards named in the
  original handoff (`navigate_point_to_point`, `deliver_object`,
  `routine_delivery`, `guidance_docent`, `high_urgency`) do show `STATE:
  APPROVED` next to `AUDITED: —`. But all 8 non-charter source cards
  (those 5 plus the 3 included scenarios) have a sibling `audit.md` with
  verdict `ready` or `ready_with_fixes`, 0 blocking — the audits genuinely
  happened. `deliver_object` and `high_urgency` were approved with 1 and 2
  open should-fix findings respectively, which the approve skill permits.
  `src/prosoc/prnc/scenarios/workflow.md:143` states the `AUDITED:`
  provenance bullet is an optional addition ("Only provenance fields that
  apply need to be included"), so its absence is a template/promotion-script
  gap, not evidence of a missing audit. **A validator should check for the
  existence and verdict of each card's `audit.md`, not the presence of the
  `AUDITED:` bullet.**

- **Golden-file staleness has a concrete, content-level cause.**
  `papers/01_charter/golden/rendered.tex` was last regenerated in PR #90
  (2026-08-12), before PR #97's charter edits (2026-08-19). This is
  independently verifiable in content, not just by commit date: the golden
  file's P1 "Explanation" prose still reads "harms people or damages
  shared environments," missing the broadened other-robots/self-damage
  language that `audit.md` records as added on the 19th. Any fresh render
  will differ from golden for two unrelated reasons at once — genuine
  defect fixes and ordinary, already-landed charter content. **Golden
  regeneration needs a manual content-diff review step, not a mechanical
  pass/fail**, to avoid conflating the two.

- **Stale pre-restructure paths are more widespread than first reported.**
  Beyond the `.claude/skills/...` reference in
  `single_file_hallway/scenario.md:9`, the pre-restructure path form
  `prosoc/<family>/...` (missing the current `src/prosoc/prnc/` prefix)
  also appears in:
  - `src/prosoc/prnc/charter/charter.md:28` — `` `prosoc/scenarios/workflow.md` ``
  - `src/prosoc/prnc/scenarios/frontal_approach/scenario.md:145` — "under prosoc/scenarios/"
  - `src/prosoc/prnc/scenarios/movable_obstruction/scenario.md:164` — "prosoc/tasks/\*/task.yml and prosoc/contexts/\*/context.yml"

  (The first pass's sweep missed these three because its exclusion grep
  — `grep -v "src/prosoc"` — also matched against the searched *file's own
  path* when multiple files were grepped at once, silently discarding every
  real hit from files under `src/prosoc/...`. Noted here so the same bug
  doesn't recur when someone re-runs the sweep.)

- **Collapsed-list defect is broader than the 5 cited spots, with two
  exclusions.** Also collapsed, same root cause: `\textbf{Geometric
  Factors} - ...` / `\textbf{Operational Factors} - ...` (6 more
  occurrences, ~lines 2261, 2265, 2555, 2559, 2848, 2851), `It frequently
  interacts with: - \textbf{P1 (Safety)}, ...` (~line 2038), and unbolded
  `Key normative expectations include: - ...` / `Common tensions include:
  - ...` (multiple occurrences). **Not** affected: `\textbf{Derived from:}`
  (its source uses trailing hard-breaks, which Pandoc renders as separate
  lines, not collapsed prose) and "such as:" (no instance of it renders as
  a collapsed list-intro anywhere in the current golden file). A
  regression test keyed to the literal string `\textbf{Includes:} -` would
  miss the unbolded cases; key detection off "label ending in a colon
  immediately followed by a hyphen-prefixed run-on" instead.

## Additional findings (not in the original handoff)

- `frontal_approach/scenario.md:6` has `**SOURCE:** Prompt to ChatGPT 5.2`
  — an internal-tooling attribution string likely worth rewording for a
  publication supplement, in the same category as the model/tool-name
  concern the handoff already raised for internal edit history generally.
- `frontal_approach/scenario.md` lists `blind_corner` as a Related
  Scenario (lines 28, 110, 146); `blind_corner` is not one of the 9
  sources in `sources.txt`, so the supplement contains a dangling
  cross-reference to content it doesn't include.
- `tests/nca/utils/papers/render_test.py` already has
  `test_rejects_unresolved_placeholders` — one item on the original
  handoff's "required tests" list is already covered.
- Across the two sandboxes used for these audits, Pandoc versions were
  3.10.1 and 2.9.2 respectively — a version gap that straddles the
  `--listings`-spelling deprecation the shared renderer's own comment
  calls out (`src/prosoc/nca/utils/papers/render.py:98`). Concrete
  illustration of the reproducibility gap the handoff flagged in general
  terms; the pipeline should pin and check the Pandoc version rather than
  trust whatever's on `PATH`.
- A live `pdflatex` test on one of the two sandboxes (not reproducible
  here — no `pdflatex` installed in this worktree) reproduced the claimed
  corruption (`P1P9`, `itselfby`, `obstructionthereby`) under a default
  build. Two details worth carrying into the fix: with `-halt-on-error`,
  `pdflatex` stops on a hard "Invalid UTF-8" error instead of silently
  mangling output (changes how the defect surfaces in CI depending on
  which fail-fast flags are chosen); and `pdftotext` with default bitmap
  fonts also dropped dashes from ordinary prose, not just the listing — any
  PDF-text regression check needs outline fonts (e.g. `lmodern`/`cm-super`)
  loaded, or it can report false results unrelated to the actual fix. Full
  character inventory actually present across the 9 sources: en dash `–`,
  em dash `—`, non-breaking hyphen `‑` (4 occurrences, in
  `single_file_hallway/scenario.md`), curly double quotes `“`/`”` (3
  pairs, in `charter.md` and `routine_delivery/context.md`). Only `–`, `—`,
  and `’` were found inside `lstlisting` blocks specifically, but mapping
  the full set in `literate=` is cheap insurance against a future edit
  landing one of the others inside a listing.

## Not independently re-verified here

Editorial/content-review items from the original handoff (`must` vs.
`should` wording consistency, P9's alignment with the overall prosocial
definition, PDF metadata, the near-empty final page) are unchanged —
neither audit pass attempted to re-litigate them. They remain scoped as
human-judgment follow-ups, not mechanical fixes, consistent with how the
original handoff already treated them.

## Net effect on implementation scope

The rendering/pipeline engineering scope (collapsed lists, heading
numbers, Unicode mapping, identifier formatting, YAML round-trip tests,
citation/stale-path cleanup, PDF build entry point, CI wiring, README fix)
is sound to implement, with the widened/narrowed detail above folded in.
The lifecycle-metadata item is narrowed to a display/bookkeeping fix plus
a validator redesign — it must not touch any card's `state:` field. The
golden-file regeneration step needs an explicit manual content-diff review
built into its process, not just a mechanical check, because the current
golden file is also stale relative to unrelated, already-landed charter
content from PR #97.
