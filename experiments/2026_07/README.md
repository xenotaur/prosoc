# 2026_07 — Packet combinatorics

Dogfoods `prosoc.packet` (the manifest-driven normative packet assembler,
`PROP-NORMATIVE-PACKET-ASSEMBLY`, adopted): demonstrates that different
(task, context, scenario) combinations produce genuinely different assembled
packets — not just different embedded raw cards, but different derived
guidance (Decision 6's principle union + emphasis annotation, and each
context's `common_tensions`).

## Why these 15 combinations

`prosoc` has no scenario→task/context reference edges (a deliberate
deferral — see the proposal's Decision 3 and Non-Goals). There is no way to
generate "reasonable" combinations mechanically; each of the 15 entries in
`scripts/combinations.py` was hand-picked and justified against the actual
task/context/scenario card content (role descriptions, principle overlap).
See that file's `rationale` field per entry for the specific justification.

Five (task, context) pairs were chosen for role coherence between the task's
stated role and the context's "Primary Role of Robot" field, out of 16
possible pairs (4 tasks × 4 contexts) — most of the other 11 are either
role-mismatched (e.g. `deliver_object` × `guidance_docent`) or redundant
with a stronger pair. Two of the five scenario groups (`deliver_object` ×
`pedestrian_overtaking` and `deliver_object` × `movable_obstruction`) are
deliberately repeated under both `routine_delivery` and `high_urgency` to
isolate context's effect: same scenario, same task, only the context
changes.

## Running it

```bash
python3 experiments/2026_07/scripts/build_manifests.py   # writes corpora/*.yml
python3 experiments/2026_07/scripts/assemble_all.py       # writes results/
```

Requires `prosoc` importable — either via `pip install -e .`
(`scripts/develop`) or run as-is; both scripts insert the repo root onto
`sys.path` themselves so no editable install is required.

Packets are assembled in dev mode (`allow_unapproved=True`, matching
`--allow-unapproved`) with a fixed justification string, since no card in
the corpus has reached `APPROVED` yet (see `WS-NORMATIVE-PACKET-ASSEMBLY`'s
still-open second exit criterion). These manifests are ad-hoc — not
registered under `prosoc/manifests/` — so they carry no STATUS block and
are not part of `prosoc-card-audit`'s coverage.

## Output

- `corpora/<id>.yml` — the 15 generated ad-hoc manifests.
- `results/packets/<id>.packet.yml` — the full assembled envelope per combo.
- `results/summary.json` — machine-readable per-combo principle
  emphasis/tensions/digest.
- `results/summary.md` — human-readable table plus a highlighted-diffs
  section that auto-detects same-scenario+task pairs differing only by
  context and shows the emphasis flip directly.

## Reading the summary table

The `emphasized`/`deprioritized` columns are driven almost entirely by
**context**, not scenario — e.g. all three `guidance_docent` rows show the
identical pattern (P2, P3, P9 emphasized; P0 deprioritized) regardless of
which scenario is paired in, because emphasis annotation is a
context-authored field (`context.principle_emphasis`), not a scenario one.
A principle present in a scenario/task's reference list but absent from the
context's emphasized/deprioritized lists shows as neutral (blank in both
columns) — e.g. `pedestrian_overtaking`'s P4 appears in neither combo's
columns above, since neither `routine_delivery` nor `high_urgency`
annotates it.

Don't read an identical emphasis pattern as "nothing changed" — the
embedded `guidance.scenarios.<id>` and `guidance.tasks.<id>` blocks differ
completely per combo; only the derived principle-emphasis view is
context-driven and can repeat across scenarios sharing a context.
