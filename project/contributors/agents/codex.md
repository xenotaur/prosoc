---
id: codex
display_name: Codex
type: agent
roles:
  - editor
status: active
execution_mode: human_orchestrated
description: >
  OpenAI Codex, observed in this fleet in two roles: an automated GitHub
  PR-review bot (`chatgpt-codex-connector`, triggered by pushes and
  explicit re-review mentions) and a cloud execution backend for
  human-submitted work (`agent: codex_cloud` in execution-record
  frontmatter). Both roles are triggered by a human action (a push, an
  explicit submission), not self-scheduled.
tools:
  - codex-cloud
  - github-code-review
---
# Codex

## Notes

- Fleet-wide policy (2026-08-09): never manually retrigger Codex's GitHub
  review role — quota-limited and slow. The automatic review that fires on
  a PR's first push is the only exception; `/lrh-self-review` substitutes
  for every subsequent round. See `DEC-*` / session memory for the
  originating decision; not yet reflected in `/lrh-confirm-fixes`'s own
  default `SKILL.md` logic as of this writing.
- `execution_mode: human_orchestrated` reflects what's actually been
  observed in this fleet (review triggered by a push or an explicit
  mention, cloud execution triggered by a human submission) — not a claim
  about Codex's own internal scheduling.
