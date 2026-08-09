---
execution_id: 2026_08_09_05_05_56_NCA_PRNC_PACKAGE_LAYOUT
prompt_id: PROMPT(AD_HOC:NCA_PRNC_PACKAGE_LAYOUT)[2026-08-09T04:29:49+00:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/85
commit: a3d308c
agent: claude_app
instruction_source: project/design/proposals/proposed/nca-prnc-package-layout/00_proposal.md
session_transcript: claude-app:f087f2be-5992-4711-b12b-40cebb7e8305
created_at: 2026-08-09T05:05:56+00:00
---

# Summary

Ran `/lrh-design` then `/lrh-proposal` for a design that separates prosoc's
verified domain-agnostic engine code (`nca`) from its PRNC-specific card
data (`prnc`/`constitutions`/`manifests`), captured as
`PROP-NCA-PRNC-PACKAGE-LAYOUT`. The design itself was worked out over a
multi-turn conversation preceding this run: an initial proposed tree, a
user-caught defect (four independent top-level packages under `src/`
instead of one), a second user-caught defect (code and data semantics
mixed flatly under one `prosoc/` package), and a final round resolving
two remaining open questions (constitutions stays un-split; a
`normative_content/` directory floated in an earlier sketch turned out to
be a misremembered phrase, not a real path — confirmed via repo-wide
grep, zero hits inside `prosoc/`).

# Result

`/lrh-design` produced the full design (prior art check, best-practices
review citing PyPA src-layout guidance/setuptools `package_data`
mechanics/PEP 420 namespace packages/spaCy-nltk data-distribution
precedent, high-level design, six enumerated low-level choices, pros/cons,
recommendation: single PR, not staged). `/lrh-proposal` then interviewed
from that existing context (no fresh Q&A needed — the design conversation
already answered every interview question), ran its own prior art check
(duplication: none in-repo; sibling-repo precedent `LogicalRoboticsHarness`
already uses this exact `src/lrh/` single-top-level-package shape,
`pyproject.toml:52-61`; demand: no existing WI/proposal/backlog entry),
passed the slug-based idempotence check (no prior record for
`nca-prnc-package-layout`), and — after the user's explicit "Confirm." —
wrote `project/design/proposals/proposed/nca-prnc-package-layout/00_proposal.md`,
opened PR #85, and created this record.

# Validation

- `lrh validate` on the new proposal file — 0 errors, 0 warnings.
- Prior art check: in-repo duplication search (`grep -rli` across
  `prosoc/`, `project/design/proposals/`, `.claude/skills/`) — zero hits.
  Demand search (`project/work_items/proposed/`,
  `project/design/proposals/proposed/`, `project/design/backlog.md`) —
  zero hits.
- Idempotence check: `lrh prompt check-execution --slug
  nca-prnc-package-layout --work-item AD_HOC` — no prior record; secondary
  `--prompt-id` check — no prior record.
- Live-repo grounding independently re-verified in this session (not
  carried from memory): `prosoc/constitutions/schema.json` has zero
  navigation/robot/social references; `packet/loader.py:23-27,33`,
  `packet/assemble.py:53,64-107,110-126`, and
  `utils/cards/validate_status.py:22-28` are the exact files/lines needing
  import-path and `REPO_ROOT`-depth fixes; `du -ck` confirmed ~800KB
  data / ~204KB code; `dist/prosoc-0.1.0-py3-none-any.whl` (Dec 2025)
  contains only `prosoc/__init__.py`, confirming no real packaging debt
  to preserve.

# Follow-up

- The proposal's own Implementation Plan is the next concrete step: a
  single PR doing the actual `git mv` + import-path fixes +
  `pyproject.toml` rewrite + CI/scripts/skill-doc updates enumerated in
  the proposal. Offered as a companion `/lrh-work-item` at the end of
  this run; not yet created — awaiting the user's decision.
- `session_transcript: pending` — update to `claude-app:f087f2be-5992-4711-b12b-40cebb7e8305`
  after the session ends.
