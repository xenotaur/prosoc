
## 2025-05-18 - jsonschema recompilation bottleneck
**Learning:** `jsonschema.validate(instance, schema)` recompiles the provided JSON schema on every single invocation which is extremely slow on hot paths or repeated validations.
**Action:** Always pre-compile the JSON schema validator instance at the module level using `jsonschema.validators.validator_for(schema)(schema)` and reuse the `.validate()` method instead of the top level `jsonschema.validate()`.
