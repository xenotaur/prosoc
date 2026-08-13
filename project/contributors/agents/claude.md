---
id: claude
display_name: Claude (Claude Code)
type: agent
roles:
  - editor
status: active
execution_mode: human_orchestrated
description: >
  AI pair-programming and design-session partner operating via Claude Code
  (Claude.app), orchestrated interactively by the human in each session —
  not independently scheduled or autonomously triggered.
tools:
  - claude-code
---
# Claude (Claude Code)

Interactive coding and design-session agent, invoked directly by the human
per session. Drives implementation, review, and control-plane bookkeeping
(execution records, work items, proposals) within a session, but does not
currently operate as an independently scheduled execution agent.

## Notes

- Human-triggered, one session at a time
- No persistent autonomous run loop
- `agent: claude_app` is the corresponding value used in execution-record
  frontmatter
