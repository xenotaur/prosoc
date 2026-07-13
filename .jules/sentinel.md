## 2026-07-06 - Mutable Action Tags in GitHub Actions
**Vulnerability:** GitHub Actions workflows (`charter.yml`, `lint.yml`, `tests.yml`) use mutable tags (`@v4`, `@v5`) for actions like `actions/checkout` and `actions/setup-python`.
**Learning:** This is a supply chain vulnerability. If the repository owner of the action updates the mutable tag to point to a malicious commit, the workflows will silently execute malicious code.
**Prevention:** Pin the action to a specific commit SHA (e.g., `@34e114876b0b11c390a56381ad16ebd13914f8d5` for checkout and `@a26af69be951a213d495a4c3e4e4022e16d87065` for setup-python) to ensure the executed code is immutable and verified.
## 2026-08-01 - Preventing Environment Leakage with dotenv
**Vulnerability:** Loading `.env` files directly into `os.environ` exposes sensitive secrets (like API keys) globally to the environment. This can leak secrets to child processes, crash reporting tools, or third-party libraries.
**Learning:** Functions that need to load specific secrets should avoid polluting the global environment namespace. `dotenv.load_dotenv()` injects variables globally, which violates the principle of least privilege.
**Prevention:** Use `dotenv.dotenv_values()` to read `.env` files into a dictionary instead of setting environment variables, and fallback to `os.getenv()` only if the key wasn't in the file.
