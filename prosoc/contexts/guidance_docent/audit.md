---
family: contexts
card: guidance_docent
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-08-02
---

# Audit: Guidance and Docent Operation

- **Card:** `prosoc/contexts/guidance_docent/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (re-audit; supersedes
  the 2026-08-01 pass, which missed the finding below)
- **Verdict:** Ready, no issues found

## Findings

### 1. `related_contexts` omitted a prose-listed entry — RESOLVED
- **Section/field:** Derived and Related Contexts (prose) vs. `related_contexts`
- **Issue (as found by PR #68 code review, `copilot-pull-request-reviewer`):**
  The 2026-08-01 pass of this audit claimed "no findings" and "all
  required schema fields are present and valid," but the card's prose
  "Derived and Related Contexts" section lists `guidance.accessibility_sensitive`
  as a third bullet, while the YAML `related_contexts` field only listed
  `baseline.public_navigation` and `service.routine_delivery` — a genuine
  one-sided claim (content in prose, absent from YAML) that the original
  pass should have caught and didn't.
- **Fix applied:** `guidance.accessibility_sensitive` added to the YAML
  `related_contexts` list, matching the prose. `context.yml` regenerated
  and confirmed in sync (`scripts/distill/contexts --dry-run --show-diffs`,
  no diff).
- **Note:** `guidance.accessibility_sensitive` does not exist yet as an
  actual context card — this is the same forward-reference pattern already
  tracked for other cards in `project/design/backlog.md`, now logged there
  for this entry too.

No other findings. `context.yml` is in sync with `context.md`. All required
schema fields are present and valid:

- `id: guidance.docent` matches the dotted-id pattern.
- `context_class: core` matches the STATUS block's `CONTEXT TYPE: CORE`.
- `primary_robot_role: guide` is a social role, not a task description.
- `applies_to_tasks: [navigate.lead_agent]` references a real task id
  (`prosoc/tasks/navigate_lead_agent/task.yml`).
- All five `axes` subsections are present, non-empty, and stay
  qualitative/descriptive rather than numeric weightings.
- `principle_emphasis` has all three required keys; every entry
  (`P2`, `P3`, `P9` emphasized; `P0` deprioritized) matches `^P[0-9]+$` and
  no principle appears in both lists.
- `P0`'s deprioritization is properly treated as an annotation, not a
  removal — the prose explicitly discusses it ("P0 (Goal Achievement) is
  reframed as successful guidance rather than mere arrival") rather than
  silently dropping it from the normative picture.
- `limits.includes`/`limits.excludes` both present and consistent with the
  prose's "Includes"/"Excludes" lists.
- `related_contexts` now matches the prose's "Derived and Related Contexts"
  bullet list exactly (see Finding 1).

Prose/YAML cross-checks (Context Summary, Context Axes Instantiated,
Relationship to Prosocial Navigation Principles, Applicability and Limits)
all agree with their corresponding YAML fields — no contradictions or drift.

## Completeness

All required sections (per `template.md`) are present and filled in:
Context Summary, Context Description, Normative Significance, Context Axes
Instantiated (all five subsections), Relationship to Prosocial Navigation
Principles, Applicability and Limits.

Optional-but-recommended sections are also filled in: Derived and Related
Contexts, Example Scenario Classes.
