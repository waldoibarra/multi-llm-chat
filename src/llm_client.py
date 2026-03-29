"""LLM client abstraction for making API calls."""

import os
from collections.abc import Iterator
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


@dataclass
class LLMResponse:
    """Represents a response from the LLM."""

    content: str
    model: str


class LLMClient:
    """Handles communication with LLM APIs."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.groq.com/openai/v1",
    ):
        load_dotenv(override=True)

        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("LLM API Key not set")

        self._client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        stream: bool = False,
    ) -> LLMResponse | Iterator[str]:
        """
        Send a chat request to the LLM.

        Args:
            model: The model identifier to use
            system_prompt: The system prompt for context
            user_prompt: The user message
            stream: Whether to stream the response

        Returns:
            LLMResponse if stream=False, Iterator[str] of chunks if stream=True
        """
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        if stream:
            return self._stream_response(model, messages)
        else:
            response = self._client.chat.completions.create(
                model=model, messages=messages
            )
            return LLMResponse(
                content=response.choices[0].message.content or "", model=model
            )

    def _stream_response(
        self, model: str, messages: list[ChatCompletionMessageParam]
    ) -> Iterator[str]:
        """Stream response chunks from the LLM."""
        stream = self._client.chat.completions.create(
            model=model, messages=messages, stream=True
        )

        for chunk in stream:
            if chunk.choices:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
