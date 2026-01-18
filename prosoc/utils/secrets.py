# prosoc/utils/secrets.py

from __future__ import annotations

import os

import dotenv

from prosoc.utils import paths


class SecretsNotFoundError(RuntimeError):
    """Raised when a required secrets file cannot be found."""


def load_openai_api_key(
    *,
    secrets_dir_name: str = ".secrets",
    env_filename: str = "openai_api_keys.env",
    env_var_name: str = "OPENAI_API_KEY",
) -> str:
    """
    Load the OpenAI API key from a .secrets directory at the repo root.

    Returns
    -------
    str
        The OpenAI API key.

    Raises
    ------
    SecretsNotFoundError
        If the secrets file or environment variable is missing.
    """

    repo_root = paths.find_repo_root()
    secrets_path = repo_root / secrets_dir_name / env_filename

    if not secrets_path.exists():
        raise SecretsNotFoundError(f"Secrets file not found: {secrets_path}")

    dotenv.load_dotenv(secrets_path)

    api_key = os.getenv(env_var_name)
    if not api_key:
        raise SecretsNotFoundError(
            f"Environment variable {env_var_name} not set "
            f"after loading {secrets_path}"
        )

    return api_key
