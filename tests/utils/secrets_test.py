import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from prosoc.utils import secrets


class TestLoadOpenAIApiKey(unittest.TestCase):
    """Unit tests for load_openai_api_key utility."""

    def test_load_openai_api_key_success(self):
        """
        load_openai_api_key should load the API key from a .secrets
        directory at the repo root.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            secrets_dir = repo_root / ".secrets"
            secrets_dir.mkdir()

            env_file = secrets_dir / "openai_api_keys.env"
            env_file.write_text("OPENAI_API_KEY=test-key-123\n")

            with mock.patch.object(
                secrets.paths, "find_repo_root", return_value=repo_root
            ):
                api_key = secrets.load_openai_api_key()

            self.assertEqual(api_key, "test-key-123")

    def test_missing_secrets_file_raises(self):
        """
        load_openai_api_key should raise SecretsNotFoundError
        if the secrets file does not exist.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)

            with mock.patch.object(
                secrets.paths, "find_repo_root", return_value=repo_root
            ):
                with self.assertRaises(secrets.SecretsNotFoundError):
                    secrets.load_openai_api_key()

    def test_missing_env_var_raises(self):
        """
        load_openai_api_key should raise SecretsNotFoundError
        if the env file exists but the variable is missing.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            secrets_dir = repo_root / ".secrets"
            secrets_dir.mkdir()

            env_file = secrets_dir / "openai_api_keys.env"
            env_file.write_text("SOME_OTHER_VAR=value\n")

            with mock.patch.object(
                secrets.paths, "find_repo_root", return_value=repo_root
            ):
                with mock.patch.dict(os.environ, {}, clear=True):
                    with self.assertRaises(secrets.SecretsNotFoundError):
                        secrets.load_openai_api_key()


if __name__ == "__main__":
    unittest.main()
