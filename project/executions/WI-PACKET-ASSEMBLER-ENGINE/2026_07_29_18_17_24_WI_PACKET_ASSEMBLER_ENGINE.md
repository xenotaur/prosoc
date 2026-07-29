---
execution_id: 2026_07_29_18_17_24_WI_PACKET_ASSEMBLER_ENGINE
prompt_id: PROMPT(WI-PACKET-ASSEMBLER-ENGINE:WI_PACKET_ASSEMBLER_ENGINE)[2026-07-29T15:41:07-04:00]
work_item: WI-PACKET-ASSEMBLER-ENGINE
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/51
commit: 308da1fa6b20739ffdbc0a2ef0c3c4c79080d716
created_at: 2026-07-29T18:17:24-04:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-PACKET-ASSEMBLER-ENGINE.md
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Implemented WI-PACKET-ASSEMBLER-ENGINE — Phase 1 of
`PROP-NORMATIVE-PACKET-ASSEMBLY`, the assembler engine that turns a
human-authored manifest into a single machine-readable guidance packet. New
`prosoc/packet/` package plus a `scripts/assemble` python -m wrapper.

# Result

Pipeline: `manifest -> resolve -> loader (single validation gate) -> fail-closed
gate -> assemble -> in-toto envelope (schema-validated)`.

- `loader.py`: generic `CardLoader` over a five-family registry ->
  `LoadedCard(family, id, path, sha256, state, payload)`, payload opaque. Schema
  validation happens only here (single runtime validation gate, per the
  `charter/loader.py` invariant); reuses `status.read_yaml_state(root_key=...)`
  so constitutions' root-wrapped state and the charter's top-level state both
  read. sha256 is over the distilled `.yml` bytes (the embedded content).
- `manifest.py` / `resolve.py`: minimal `family`+`id` manifest -> ordered
  `LoadedCard`s (dangling member -> `ResolveError`).
- `gate.py`: fail-closed. Production order DRAFTED<EDITED<AUDITED<APPROVED<
  VALIDATED, default floor APPROVED; DEPRECATED/RETIRED never ship.
  `--allow-unapproved` lowers the floor and the bypass is stamped into the
  payload (`predicate.policy.escape_hatch` + `guidance.notice`), so a
  development packet is not byte-indistinguishable from a production one.
- `assemble.py`: namespaced envelope, never a deep merge — verified the
  `scenario.context:` inline key does not collide with a context card. `guidance`
  (state stripped, family root keys normalized, Decision-6 principle union with
  `emphasis: emphasized|deprioritized|neutral` — none dropped — and both
  `common_tensions` and `conflict_resolution` surfaced) + `predicate` (builder +
  per-card id/family/path/sha256/state). `subject.digest` covers the serialized
  `guidance` only; reserved DSSE `signatures: []`. Output is schema-validated.
- `schema.json`: the packet envelope schema.
- `tests/packet/`: loader (real corpus, all five families), manifest, resolve,
  gate, assemble (namespacing/no-collision, state strip, principle union +
  emphasis, digest, escape-hatch stamping + justification requirement), and a
  CLI integration test on the checked-in sample manifest.

Design decisions settled at implement time: manifest member id = the card
directory locator (payload keeps its own semantic id); sha256 over the `.yml`;
gate thresholds APPROVED (prod) / any-live (dev); escape hatch stamped only when
the packet actually contains a sub-APPROVED card. Prior-art check present in the
WI. No normative card content changed.

# Validation

- `scripts/test`: 186 passed (+47 packet tests).
- `scripts/lint`: All checks passed.
- `scripts/format --check` (black 25.12.0): clean (68 files unchanged).
- `lrh validate`: 0 errors, 0 warnings.
- `scripts/validate/status`: all 31 cards consistent.
- `scripts/assemble <sample>`: fail-closed (emits nothing, exit 1);
  `--allow-unapproved "<why>"`: emits a schema-valid, hatch-stamped packet.

# Follow-up

- At closeout, resolve WI-PACKET-ASSEMBLER-ENGINE (the engine deliverable is
  done). The workstream stays open for Phases 0b (audit skills), 2 (manifest
  card family), and 3 (CI packet-drift check).
- A brief interruption during implementation from a transient Anthropic-side
  model outage affected the safety classifier (Bash/Edit); it did not affect the
  code, which was completed and then validated once tools recovered.

# Summary

TODO: Briefly summarize the intended prompt-driven work.

# Result

TODO: Fill in what happened.

# Validation

TODO: List tests or checks run.

# Follow-up

TODO: List deferred work.
