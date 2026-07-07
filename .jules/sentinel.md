## 2026-07-06 - Mutable Action Tags in GitHub Actions
**Vulnerability:** GitHub Actions workflows (`charter.yml`, `lint.yml`, `tests.yml`) use mutable tags (`@v4`, `@v5`) for actions like `actions/checkout` and `actions/setup-python`.
**Learning:** This is a supply chain vulnerability. If the repository owner of the action updates the mutable tag to point to a malicious commit, the workflows will silently execute malicious code.
**Prevention:** Pin the action to a specific commit SHA (e.g., `@34e114876b0b11c390a56381ad16ebd13914f8d5` for checkout and `@a26af69be951a213d495a4c3e4e4022e16d87065` for setup-python) to ensure the executed code is immutable and verified.
