---
family: manifests
card: sample_packet
verdict: ready
blocking: 0
should_fix: 1
suggestion: 0
audited: 2026-08-07
---

# Audit: Sample Packet

- **Card:** `prosoc/manifests/sample_packet/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-07 (fresh audit —
  prior audit dated 2026-07-30 was stale relative to the corpus's actual
  progression; the manifest's own files weren't touched again until this
  pass, but all five of its members have since been promoted to
  `APPROVED`, and PR #79 regenerated `packet.golden.yml` to reflect the
  charter's final `APPROVED` promotion without updating this card's own
  prose)
- **Verdict:** Ready for `AUDITED` once the should-fix below is applied.

## Findings

### 1. Manifest Description misdescribes current assembler behavior — should-fix
- **Section/field:** `## Manifest Description` prose vs. live
  `scripts/assemble` behavior
- **Issue:** The Description reads: "The whole corpus is currently
  `DRAFTED`, so `scripts/assemble` on this manifest is fail-closed by
  default and emits nothing; pass `--allow-unapproved "<why>"` to produce
  a non-production packet stamped with the escape-hatch marker." This was
  accurate on 2026-07-30 (confirmed by the prior audit's Member
  Resolvability table, which correctly showed all five members
  pre-`APPROVED`). It is no longer true: all five members
  (`charter/charter`, `constitutions/asimov_three_laws`,
  `scenarios/intersection_gesture_wait`, `tasks/navigate_lead_agent`,
  `contexts/high_urgency`) are now `APPROVED`. Verified live: `scripts/assemble
  prosoc/manifests/sample_packet/manifest.yml` (no `--allow-unapproved`)
  succeeds and emits a full packet with `policy.allow_unapproved: false`
  and every `resolved_cards[].state: APPROVED`; `--check` confirms this
  matches `packet.golden.yml` exactly (byte-for-byte, exit 0) — the
  golden file was itself regenerated in PR #79 when the charter reached
  `APPROVED`, but the Description prose wasn't updated at the same time.
- **Recommended fix:** Reword the Description to state that all five
  members are currently `APPROVED` and `scripts/assemble` succeeds by
  default without the escape hatch, while still documenting
  `--allow-unapproved` as available for future non-production use if any
  member is later reverted below `APPROVED`.

## Merge-integrity check (user-requested)

The user flagged possible merge issues affecting this card and asked for
a thorough re-check, not just the staleness finding above. Checked
explicitly:
- `grep -rn '<<<<<<<\|=======\|>>>>>>>' prosoc/manifests/sample_packet/`
  — no merge-conflict markers found.
- `manifest.yml` (distilled) matches `manifest.md`'s embedded YAML
  exactly — `scripts/distill/manifests --dry-run --show-diffs` reports no
  diff.
- `packet.golden.yml` matches live `scripts/assemble ... --check` output
  exactly (exit 0, no drift).
- `scripts/test` (239 tests) and `lrh validate` both clean.
- `git log --oneline -- prosoc/manifests/sample_packet/` shows the last
  real content touch was PR #65 (pilot promotion) plus PR #79's
  golden-regeneration commit — no partial/conflicting edits, no orphaned
  hunks.

No merge damage found. The only issue is the pre-existing prose
staleness in Finding 1, which predates PR #79 and was simply never
caught until this pass.

## Prose/YAML Consistency

Manifest Summary (`Manifest ID: sample_packet`, `Manifest Name: Sample
Packet`, `Builder: prosoc packet assembler (sample)`, `Member Count: 5`)
matches `id`, `name`, `builder`, and `len(members)` exactly. The Members
section lists 5 bullets, one per `members[]` entry, with no prose bullet
lacking a YAML counterpart or vice versa. Unaffected by Finding 1 (which
is confined to the Manifest Description section).

## Schema Compliance

- `scripts/distill/manifests --dry-run --show-diffs` produced no diff and
  no schema validation error (sole card in the family).
- `members[]` has only `family`/`id` per entry; no `additionalProperties`
  violations.
- No `members[].family` is `manifests` — all five are valid content
  families.
- No duplicate `{family, id}` pairs.

## Member Resolvability

All five members resolve and load via `prosoc.packet.loader.load_card`:

| Member | Resolves | State |
|---|---|---|
| `charter/charter` | Yes | APPROVED |
| `constitutions/asimov_three_laws` | Yes | APPROVED |
| `scenarios/intersection_gesture_wait` | Yes | APPROVED |
| `tasks/navigate_lead_agent` | Yes | APPROVED |
| `contexts/high_urgency` | Yes | APPROVED |

No dangling members. All five member states are now `APPROVED` —
`scripts/assemble` on this manifest succeeds by default (no
`--allow-unapproved` needed), confirmed live and matching
`packet.golden.yml`. This supersedes the 2026-07-30 audit's table, which
correctly showed all members pre-`APPROVED` at that time.

## Completeness

Manifest Summary, Manifest Description, and Members are all present and
populated. No blank required fields. Finding 1 is a factual-accuracy
issue in populated prose, not a completeness gap.
