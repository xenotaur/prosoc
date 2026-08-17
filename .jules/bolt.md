## $(date +%Y-%m-%d) - jsonschema recompilation bottleneck
**Learning:** `jsonschema.validate(instance, schema)` compiles the schema from scratch on every call. In loops or high-throughput paths (like packet loading or test suites with many cards), this causes severe performance bottlenecks.
**Action:** When validating JSON schemas repeatedly, always pre-compile the validator using `jsonschema.validators.validator_for(schema)(schema)` and cache it via `@functools.cache` or manual memoization.
