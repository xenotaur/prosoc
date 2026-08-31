## 2024-06-25 - Prevent Top-Level Schema Recompilation
**Learning:** `jsonschema.validate(instance, schema)` called inside hot paths recompiles the JSON schema on every single invocation, causing significant CPU overhead and high latency when validating large documents or repeating validation.
**Action:** Replace `jsonschema.validate` with a pre-compiled validator using `jsonschema.validators.validator_for(schema)(schema)` and cache it (either at the module level or with `@functools.lru_cache`).
