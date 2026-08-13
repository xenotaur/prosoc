---
id: antigravity
display_name: Antigravity
type: agent
roles:
  - editor
status: active
execution_mode: human_orchestrated
description: >
  Google's Antigravity coding agent. Recognized as a distinct install
  target in LRH's own skill-installer tooling (`SkillTarget.ANTIGRAVITY`,
  `src/lrh/skills/installer.py`), confirming it as a first-class fleet
  member — but this fleet's records don't yet document its own runtime
  execution semantics beyond that install-time differentiation.
  `execution_mode: human_orchestrated` is a conservative default, not a
  verified characterization; correct it if that turns out to be wrong.
tools:
  - antigravity
---
# Antigravity

## Notes

- Confirmed as a real, distinct fleet member via LRH's `SkillTarget` enum
  (`claude`/`codex`/`antigravity`), not yet via direct observation of its
  own execution behavior in this fleet's records.
