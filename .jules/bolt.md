## 2024-05-24 - jsonschema recompilation overhead
**Learning:** Calling `jsonschema.validate(instance, schema)` is a major bottleneck in a loop because it recompiles the schema validation logic every time. This is especially impactful in data loaders and builders.
**Action:** When working with `jsonschema`, always use `validator_cls = jsonschema.validators.validator_for(schema)` and cache the instantiated `validator_cls(schema)` so that `validator.validate(instance)` avoids recompilation overhead on subsequent calls.
