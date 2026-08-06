"""
OpenAI client adapter for the Prosoc auditor.

This module provides a thin, testable wrapper around the OpenAI API that
implements the LLM client interface expected by audit_normative_card().

Design goals:
- Deterministic JSON-only output
- Clear separation between transport and audit logic
- No schema knowledge in this layer
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from openai import OpenAI


class OpenAIClient:
    """
    OpenAI LLM client adapter.

    This class exposes a single method, complete(), which matches the
    interface expected by the auditor orchestration layer.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        organization: Optional[str] = None,
        default_model: str = "gpt-4.1",
        temperature: float = 0.0,
        timeout: float = 60.0,
    ):
        # Security: Added timeout to prevent infinite hanging on API calls
        self._client = OpenAI(
            api_key=api_key,
            organization=organization,
            timeout=timeout,
        )
        self._default_model = default_model
        self._temperature = temperature

    def complete(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        model_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute a completion request against the OpenAI API and return
        parsed JSON output.

        Parameters
        ----------
        system_prompt : str
            System role prompt.
        user_prompt : str
            User role prompt containing task instructions and data.
        model_name : str, optional
            Model identifier. If None or "default", uses the client's
            default model.

        Returns
        -------
        dict
            Parsed JSON object returned by the model.

        Raises
        ------
        ValueError
            If the model output cannot be parsed as valid JSON.
        """

        model = (
            self._default_model
            if model_name is None or model_name == "default"
            else model_name
        )

        response = self._client.chat.completions.create(
            model=model,
            temperature=self._temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(
                "OpenAI response was not valid JSON. "
                "This indicates a prompt or model failure."
            ) from e
