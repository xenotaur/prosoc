---
family: constitutions
card: asimov_four_laws
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-08-08
---

# Audit: Asimov's Four Laws of Robotics

- **Card:** `prosoc/constitutions/asimov_four_laws/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-08 (fresh pass —
  the 2026-08-01 audit found zero issues; this pass adds one new finding
  surfaced at the `APPROVED` human-accountability gate itself, not by
  the automated audit checks)
- **Verdict:** Ready, no blocking or should-fix issues found

## Findings

### 1. `scope.exclusions` claims are contested, not factually wrong — suggestion, documented in this pass
- **Section/field:** `scope.exclusions` (`military_combat`,
  `self-modifying_agents`) vs. `## Discussion`
- **Issue:** At the `APPROVED` review, the user (domain expert) raised
  two substantive objections: (1) a combat robot bound by these Laws
  wouldn't be excluded from the domain, it would simply be forbidden
  from lethal action — a real, evaluable constraint, not an
  out-of-scope case; (2) the `self-modifying_agents` exclusion assumes
  self-modification is inherently incompatible with a fixed rule
  hierarchy, but (citing Hofstadter's *Gödel, Escher, Bach* Gödelian
  self-reference argument) a self-modifying agent could still carry an
  immutable constitutional core, making the blanket exclusion broader
  than the underlying concern. Neither objection identifies a factual
  transcription error (unlike, e.g., `following`'s Table 3 erratum) —
  both are genuinely open interpretive questions about how to scope a
  "canonical historical baseline" constitution.
- **Resolution (Option C, user-selected):** rather than editing the
  `scope.exclusions` list itself — which would require picking a side
  in an active, still-debatable question and would leave the identical
  exclusions on the sibling `asimov_three_laws` card (already
  `APPROVED`) silently inconsistent — added a "Contested scope claims"
  bullet to `## Discussion` capturing both objections in full, alongside
  the card's existing "Known ambiguities" and "Ethical tradeoffs"
  bullets. This is prose-only (outside the fenced YAML block);
  `scripts/distill/constitutions --dry-run --show-diffs` confirmed no
  diff. `asimov_three_laws` carrying the same unresolved claims is
  logged separately in `project/design/backlog.md`'s "APPROVED cards
  with unresolved findings" table.

## Prose/YAML Consistency

Unchanged from the 2026-08-01 pass — re-confirmed: `## Discussion`'s
Known ambiguities / Assumptions about environment / Ethical tradeoffs /
Contested scope claims are all top-level parallel bullets matching
`template.md`'s pattern; `rules[3]` (`L3`)'s `should`-level phrasing
still matches its `type`/`priority`/`rationale`. `constitution.yml` is
in sync with `constitution.md`'s embedded YAML (no diff).

## Schema and Charter Compliance

Unchanged: fenced YAML correctly root-wrapped under `constitution:`;
`id`/`name`/`state`/`rules` present; every `rules[].type` is
`must`/`must_not`/`should`, every `priority` is `high`/`medium`/`low`; no
two rules directly contradict; `conflict_resolution` explicitly orders
both `high`-priority rules (`L0` overrides `L1`).

## Completeness

All required fenced-YAML fields present: `id`, `name`, `state`, `rules`
(4 rules, each with `id`/`text`/`type`/`priority`). STATUS block present
with `STATE` as the first bullet. Optional-but-recommended content is
filled in throughout: `scope`, every rule's
`rationale`/`examples`/`evaluation_tags`, `conflict_resolution`, and
`## Discussion` (now including the Contested scope claims bullet).
