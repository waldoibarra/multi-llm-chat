"""Speaker classes for the conversation."""

import json
from dataclasses import dataclass

from rich.console import Console
from rich.markdown import Markdown

from src.config import CONVERSATION_GOAL, SpeakerConfig, get_speaker_by_name
from src.llm_client import LLMClient

ChatHistory = list[tuple[str, str]]


@dataclass
class SpeakerResponse:
    """Represents a speaker's response."""

    message: str
    requesting_reply_from: str | None  # None means random


class Speaker:
    """Represents a participant in the conversation."""

    def __init__(
        self,
        config: SpeakerConfig,
        llm_client: LLMClient,
        console: Console | None = None,
    ):
        self.config = config
        self.llm_client = llm_client
        self.console = console or Console()

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def model(self) -> str:
        return self.config.model

    def format_prompt(self, chat_history: ChatHistory) -> str:
        """Format the user prompt with chat history context."""

        if not chat_history:
            history = "Nadie ha dicho nada aún, es tu oportunidad de brillar."
        else:
            history = "\n".join(
                f"* **{speaker}**: {message}" for speaker, message in chat_history
            )

        return (
            "## Objetivo de la conversación\n\n"
            f"{CONVERSATION_GOAL}\n\n"
            "## Historial del chat\n\n"
            f"{history}\n\n"
            "## Formato de respuesta\n\n"
            "Responde ÚNICAMENTE con JSON válido."
        )

    def speak(self, chat_history: ChatHistory) -> SpeakerResponse:
        """
        Have this speaker respond to the conversation.

        Args:
            chat_history: The conversation history (speaker, message) tuples

        Returns:
            SpeakerResponse with message and next speaker request
        """
        # Header with speaker name
        self.console.print(Markdown(f"\n### {self.name}"))

        user_prompt = self.format_prompt(chat_history)

        # Get complete response (non-streaming)
        response_obj = self.llm_client.chat(
            model=self.model,
            system_prompt=self.config.system_prompt,
            user_prompt=user_prompt,
            stream=False,
        )

        raw_response = response_obj.content  # type: ignore[union-attr]

        # Parse JSON response
        speaker_response = self._parse_json_response(raw_response)

        # Log beautifully
        self._display_response(speaker_response)

        # Add to chat history (store the message, not the JSON)
        chat_history.append((self.name, speaker_response.message))

        return speaker_response

    def _display_response(self, response: SpeakerResponse) -> None:
        """Display the response beautifully."""
        # The message in markdown
        self.console.print(Markdown(f"{response.message}", style=self.config.color))

        # Show who they're requesting (if any)
        if response.requesting_reply_from:
            self.console.print(
                Markdown(
                    f"\n-> Pidiendo respuesta a {response.requesting_reply_from}",
                    style="dim",
                )
            )

    def _parse_json_response(self, raw_response: str) -> SpeakerResponse:
        """Parse JSON response from the LLM."""
        try:
            # Try to find JSON in the response (in case there's extra text)
            json_start = raw_response.find("{")
            json_end = raw_response.rfind("}") + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")

            json_str = raw_response[json_start:json_end]
            data = json.loads(json_str)

            message = data.get("message", "")
            requesting_reply_from = data.get("requesting_reply_from")

            # Validate that requesting_reply_from is a valid speaker name or null
            if requesting_reply_from is not None:
                if get_speaker_by_name(requesting_reply_from) is None:
                    # Invalid speaker name, treat as random
                    requesting_reply_from = None

            return SpeakerResponse(
                message=message,
                requesting_reply_from=requesting_reply_from,
            )

        except (json.JSONDecodeError, ValueError):
            # If JSON parsing fails, treat the entire response as the message
            return SpeakerResponse(
                message=raw_response,
                requesting_reply_from=None,
            )
