# Manifest: <Human-Readable Manifest Name>

## STATUS
- **STATE:** DRAFTED
- **SOURCE:** <what this manifest packages, and why>
- **DRAFTED:** <author or system, date>
- **EDITED:** <optional>
- **AUDITED:** <optional>
- **VALIDATED:** <optional>

---

## Manifest Summary

> **Required**

- **Manifest ID:** <canonical_manifest_id>
- **Manifest Name:** <concise human-readable name>
- **Builder:** <identity of the entity assembling packets from this manifest>
- **Member Count:** <number of members>

---

## Manifest Description

> **Required**

Provide a clear, human-readable description of the packet this manifest
assembles, including:
- what downstream agent or purpose the assembled packet serves,
- why these particular member cards were chosen together,
- and what makes this manifest distinct from other manifests.

---

## Members

> **Required**

List each member card by family and id, with a one-line note on why it is
included:

- `<family>/<id>` — <why this card belongs in the packet>

A manifest names members by `family` + the member's locator `id` within that
family (its directory name, or `charter` for the single-source charter
family). A manifest must never name another manifest as a member.

---

## Manifest Specification (Machine-Readable)

> **Required**

```yaml
id: <canonical_manifest_id>
name: <Human-Readable Manifest Name>
state: DRAFTED

builder: <identity of the entity assembling packets from this manifest>

members:
  - {family: <scenarios|tasks|contexts|constitutions|charter>, id: <member_id>}
```
