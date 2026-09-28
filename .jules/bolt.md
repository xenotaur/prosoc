## 2024-05-18 - Avoid Top-Level jsonschema.validate
**Learning:** Using top-level `jsonschema.validate(instance, schema)` inside loops or hot paths recompiles the schema and repeatedly reads the schema from disk, leading to significant performance bottlenecks.
**Action:** When using `jsonschema` for validation, pre-compile and cache the validator instance using `jsonschema.validators.validator_for(schema)(schema)`. Use `@functools.lru_cache` to cache schema JSON parsing from disk to ensure it's only done once.
