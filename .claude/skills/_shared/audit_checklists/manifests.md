# Prosoc Manifest Audit Checklist

This is a verification rubric, companion to `src/prosoc/manifests/schema.json`
and `src/prosoc/manifests/template.md`. Unlike the five content families, a
manifest's primary risk is not prose/YAML content drift — it is
**resolvability**: whether every member the manifest names actually exists
and is loadable by `prosoc.nca.packet.resolve`. Read `../principles.md` only if a
member's family-specific checks require it (a manifest itself has no
principle-reference fields).

## Required Fields (schema.json)

| Field | Check |
|-------|-------|
| `id` | Matches `^[a-z][a-z0-9_]*$`, matches the directory name |
| `name` | Matches the manifest's title heading in `manifest.md` |
| `members` | Non-empty array |
| `members[].family` | One of `scenarios`, `tasks`, `contexts`, `constitutions`, `charter` — **never `manifests`** |
| `members[].id` | The member's locator id within its family |

## Prose/YAML Cross-Checks

| Prose section | Cross-check against YAML field(s) |
|---|---|
| Manifest Summary | `id`, `name`, `builder`, member count vs. `len(members)` |
| Members | `members[]` — every prose bullet should have a matching
  `{family, id}` entry, and vice versa |

Flag a **contradiction** when the prose Members list and the YAML `members`
list disagree on which cards are included (a bullet with no YAML entry, or a
YAML entry with no prose bullet). Flag **drift** when the prose's stated
member count doesn't match `len(members)`.

## Schema Compliance

- [ ] `manifest.yml` validates against `schema.json` (no `additionalProperties`
      violations; each `members[]` entry has only `family`/`id`)
- [ ] `members[].family` is never `manifests` — a manifest naming another
      manifest as a member would make `prosoc.nca.packet.resolve` recursive in a
      way the engine is not designed for (`schema.json`'s `enum` already
      excludes it structurally; treat any occurrence as **blocking**, not a
      should-fix, since it cannot be resolved correctly)
- [ ] No duplicate `{family, id}` pairs within `members`

## Member Resolvability (manifest-specific — the primary audit concern)

For each `members[]` entry, verify the referenced card actually exists and
loads:

- [ ] The family is one of the five registered content families
      (`prosoc.nca.packet.loader.FAMILIES`)
- [ ] The card resolves under that family — for card-per-directory families
      (`scenarios`, `tasks`, `contexts`, `constitutions`), a directory named
      `id` exists with the family's card file; for `charter`, `id` is
      literally `"charter"` (the single-source family has no other valid id)
- [ ] The referenced card's own `state` (not the manifest's) is worth noting
      in the audit if it is markedly different from what the manifest's
      purpose implies (e.g. a manifest intended for production use naming a
      `DRAFTED` member) — this is informational, not something the manifest
      audit itself blocks on, since the packet assembler's own fail-closed
      gate is the enforcement point for member state, not the manifest audit

A dangling member (family/id that does not resolve) is a **blocking**
finding — `prosoc.nca.packet.resolve` will raise a `ResolveError` at assembly
time, so an unresolvable manifest cannot produce a packet at all.

## Completeness (template.md "Required" sections)

- [ ] Manifest Summary (Manifest ID, Manifest Name, Builder, Member Count)
- [ ] Manifest Description
- [ ] Members (one bullet per member, each with a stated reason for inclusion)

For each blank required field/section, decide reasonably blank (genuinely not
yet applicable — rare for a manifest, since every field here is structural)
vs. should probably be filled in now.
