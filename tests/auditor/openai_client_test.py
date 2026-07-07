import json
import unittest
from unittest import mock

from prosoc.auditor.openai_client import OpenAIClient


class _FakeOpenAIResponse:
    """Minimal fake OpenAI response object matching the accessed shape."""

    def __init__(self, content: str):
        self.choices = [
            mock.Mock(
                message=mock.Mock(
                    content=content,
                )
            )
        ]


class TestOpenAIClient(unittest.TestCase):
    """Unit tests for the OpenAIClient adapter."""

    def setUp(self):
        # Patch the OpenAI constructor inside the module
        self.patcher = mock.patch("prosoc.auditor.openai_client.OpenAI")
        self.mock_openai_cls = self.patcher.start()
        self.addCleanup(self.patcher.stop)

        # Create a mock client instance
        self.mock_openai_instance = self.mock_openai_cls.return_value
        self.mock_chat = self.mock_openai_instance.chat
        self.mock_completions = self.mock_chat.completions

    def test_complete_returns_parsed_json(self):
        """
        complete() should return a parsed JSON object when the model
        returns valid JSON content.
        """
        response_json = {"status": "ok", "value": 123}
        fake_response = _FakeOpenAIResponse(json.dumps(response_json))

        self.mock_completions.create.return_value = fake_response

        client = OpenAIClient(default_model="gpt-test")

        result = client.complete(
            system_prompt="system",
            user_prompt="user",
            model_name="default",
        )

        self.assertEqual(result, response_json)

    def test_complete_invalid_json_raises_value_error(self):
        """
        complete() should raise ValueError if the model output
        is not valid JSON.
        """
        fake_response = _FakeOpenAIResponse("not-json")
        self.mock_completions.create.return_value = fake_response

        client = OpenAIClient(default_model="gpt-test")

        with self.assertRaises(ValueError):
            client.complete(
                system_prompt="system",
                user_prompt="user",
                model_name="default",
            )

    def test_default_model_is_used_when_model_name_is_none(self):
        """
        If model_name is None, the client's default_model should be used.
        """
        fake_response = _FakeOpenAIResponse("{}")
        self.mock_completions.create.return_value = fake_response

        client = OpenAIClient(default_model="gpt-default")

        client.complete(
            system_prompt="system",
            user_prompt="user",
            model_name=None,
        )

        _, kwargs = self.mock_completions.create.call_args
        self.assertEqual(kwargs["model"], "gpt-default")

    def test_explicit_model_name_overrides_default(self):
        """
        If an explicit model_name is provided, it should override
        the client's default_model.
        """
        fake_response = _FakeOpenAIResponse("{}")
        self.mock_completions.create.return_value = fake_response

        client = OpenAIClient(default_model="gpt-default")

        client.complete(
            system_prompt="system",
            user_prompt="user",
            model_name="gpt-explicit",
        )

        _, kwargs = self.mock_completions.create.call_args
        self.assertEqual(kwargs["model"], "gpt-explicit")

    def test_timeout_is_passed_to_openai_client(self):
        """
        The timeout parameter should be passed to the underlying
        OpenAI client constructor.
        """
        OpenAIClient(timeout=42.0)

        _, kwargs = self.mock_openai_cls.call_args
        self.assertEqual(kwargs["timeout"], 42.0)


if __name__ == "__main__":
    unittest.main()
