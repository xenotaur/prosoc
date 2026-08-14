# prosoc.utils.cards — corpus review-queue engine

Ranks prosoc normative cards by what most needs review, and is the
mechanism behind the human-facing card-promotion skills. Built by
`WI-CARD-APPROVE-SKILLS`, first exercised end-to-end by
`WI-CARD-APPROVAL-PILOT` (see `PROP-NORMATIVE-CARD-APPROVAL` for the design
rationale). This doc is the human walkthrough for actually running a
promotion session — the `.claude/skills/prosoc-card-*` `SKILL.md` files are
the agent-facing operating instructions this doc's steps dispatch to.

## Why this exists

Every card in the corpus moves through a lifecycle — the full chain is
`SOURCE → DRAFTED → EDITED → AUDITED → APPROVED → VALIDATED →
DEPRECATED/RETIRED`, defined in `prosoc/scenarios/workflow.md`; this doc
and its skills are only concerned with the `DRAFTED`/`EDITED` → `AUDITED` →
`APPROVED` segment. `AUDITED` is a machine-assisted finding pass
(`/prosoc-card-audit`); `APPROVED` is a **human accountability attestation**
and must not be conflated with it. As of `WI-CARD-APPROVAL-PILOT`, only the
5-card `sample_packet` pilot has reached `APPROVED`; the other 27 cards in
the corpus (as of this writing) are still below that floor, several with no
audit evidence at all. Promoting them one at a time by hand doesn't scale
and gives no way to prioritize — this engine and the skills built on it are
how a human works through the rest of the corpus in a structured session.

## The three skills, and which one you actually invoke

- **`/prosoc-card-approve`** — mechanical, single-card, single-step state
  edit. You won't normally call this directly; it's the primitive the other
  two delegate to once a human has decided to promote.
- **`/prosoc-card-review`** — one card, one lifecycle step, with an
  independent recommendation and a confirm gate before anything is edited.
  Use this when you already know which single card you want to work on.
- **`/prosoc-card-review-all`** — walks the whole corpus (or one family) in
  priority order, calling `/prosoc-card-review` per card. **This is the one
  to invoke for a full-corpus promotion session.**

## Running a session

1. **Invoke the skill**, e.g. in chat: `/prosoc-card-review-all` (whole
   corpus), `/prosoc-card-review-all scenarios` (one family), or
   `/prosoc-card-review-all --limit 5` (bound the session length — good for
   a first run). These compose: `/prosoc-card-review-all scenarios --limit 5`
   works too.
2. **You'll be shown the ranked queue** before anything is touched — see
   the CLI section below for what the ranking means. This is where you
   decide how much of the queue to take on this session, if `--limit`
   wasn't already given.
3. **For each card, in ranked order**, the skill checks whether its
   `audit.md` is missing or stale and runs `/prosoc-card-audit` first if
   so (no separate gate for this — it's non-destructive), then presents an
   independent recommendation and **stops for your decision**: promote,
   hold, or address findings first. Nothing is edited without your
   explicit go-ahead, one card at a time.
4. **You can stop early** at any point ("that's enough for today") — the
   session reports progress on whatever was reviewed so far rather than
   forcing the full queue.
5. **At the end**, the session aggregates a before/after/outcome table,
   optionally offers to write a point-in-time snapshot to
   `project/audits/CARD_REVIEW_SUMMARY.md`, then branches, commits every
   card actually promoted this session, and opens a PR. Landing that PR
   (review, merge) is a separate, ordinary human decision — the skill does
   not merge its own PR.

## The ranked queue (CLI reference)

The skills call this under the hood; you can also run it directly to see
the current state of the corpus without starting a review session:

```bash
scripts/validate/review-queue [--family NAME] [--sort FIELDS] [--order asc|desc,...] [--format table|json] [--limit N]
```

- `--family` restricts to one of `charter`, `constitutions`, `contexts`,
  `manifests`, `scenarios`, `tasks` (omit for all six).
- `--sort`/`--order` are comma-separated, most-significant field first
  (`severity,scope` descending is the default — usually leave this alone).
- `--format json` for scripting; `table` (default) for reading directly.
- `--limit N` shows only the top `N` rows after sorting.

Ranking, in order of what it means for you:

- **`SEV` (severity)** — weighted sum of the card's `audit.md` finding
  counts (blocking outranks any number of should-fix, should-fix outranks
  any number of suggestions). A card with **no `audit.md` at all** gets a
  large sentinel severity value, intended to outrank any realistic weighted
  sum (`AUDIT` column reads `NO` in the table) — it can't even be assessed
  for promotion yet, so it surfaces first.
- **`SCOPE`** — how many lifecycle steps remain to `APPROVED` (0 means
  already there).

Example output — a snapshot taken at time of writing (32 cards total, 5
already `APPROVED`); run the command yourself for the current state, since
counts shift as cards are promoted:

```
FAMILY         ID                   STATE      SCOPE     SEV AUDIT  VERDICT
contexts       guidance_docent      DRAFTED        3 1000000 NO     -
contexts       public_navigation    DRAFTED        3 1000000 NO     -
contexts       routine_delivery     DRAFTED        3 1000000 NO     -
constitutions  asimov_four_laws     EDITED         2 1000000 NO     -
tasks          deliver_object       DRAFTED        3      20 yes    ready_with_fixes
...
charter        charter              APPROVED       0      20 yes    ready_with_fixes
```

The four rows with `AUDIT` = `NO` (`asimov_four_laws`, `guidance_docent`,
`public_navigation`, `routine_delivery`) sort first for exactly this reason
— expect `/prosoc-card-review` to kick off a `/prosoc-card-audit` pass on
each of those before it can offer a promotion recommendation.

## Worked example

`WI-CARD-APPROVAL-PILOT`'s execution record
(`project/executions/WI-CARD-APPROVAL-PILOT/2026_07_31_20_58_37_WI_CARD_APPROVAL_PILOT.md`)
is a full worked example of this process end to end — re-verifying audit
currency, forming per-card recommendations, batching the confirm gate, and
regenerating a manifest's golden packet once every member reached
`APPROVED` — for the pilot's 5 cards specifically. The mechanics are
identical for the remaining corpus; only the scale differs.

## What this doesn't do

- Doesn't change the lifecycle definition or the packet gate's production
  order — see `prosoc/scenarios/workflow.md` and `prosoc/packet/README.md`.
- Doesn't merge or approve its own PR — landing stays a separate human
  decision.
- Doesn't maintain a live dashboard — the optional summary snapshot is
  regenerated wholesale on request, not continuously updated.
