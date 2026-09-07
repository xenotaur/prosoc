## 2026-09-07 - jsonschema recompilation bottleneck
**Learning:** Top-level `jsonschema.validate(instance, schema)` parses and compiles the schema on every call, creating a huge bottleneck in hot paths (like looping over JSON files).
**Action:** Use `jsonschema.validators.validator_for(schema)(schema)` to create a pre-compiled validator, cache it (e.g. with `functools.lru_cache` or module-level variables), and call `.validate(instance)` on it.
