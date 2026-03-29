"""Conversation orchestration."""

import random

from rich.console import Console
from rich.markdown import Markdown

from src.config import CONVERSATION_GOAL, CONVERSATION_ROUNDS
from src.speakers import ChatHistory, Speaker


class ConversationOrchestrator:
    """Manages the flow of the multi-speaker conversation."""

    def __init__(self, speakers: list[Speaker], console: Console | None = None):
        self.speakers = speakers
        self.console = console or Console()
        # Create a lookup map for speakers by name
        self._speaker_by_name: dict[str, Speaker] = {s.name: s for s in speakers}

    def format_conversation_display(self, chat_history: ChatHistory) -> str:
        """Format the conversation for display."""
        conversation = "# Conversación\n\n"
        conversation += "## Objetivo de la conversación\n\n"
        conversation += f"{CONVERSATION_GOAL}\n\n"
        conversation += "---\n\n"

        if not chat_history:
            return conversation

        conversation += "## Mensajes previos\n\n"
        conversation += "\n".join(
            # TODO: Might want to style the speaker message with the assigned color.
            f"### {speaker}\n\n{message}\n"
            for speaker, message in chat_history
        )
        conversation += "\n---\n\n"

        return conversation

    def _get_next_speaker(
        self,
        current_speaker: Speaker,
        requested: str | None,
        spoken: set[str],
    ) -> Speaker:
        """
        Determine the next speaker based on request and who has already spoken.

        Args:
            current_speaker: The speaker who just spoke
            requested: The name of the requested next speaker (can be None)
            spoken: Set of speaker names who have already spoken this round

        Returns:
            The next speaker to speak
        """
        # If a specific person was requested and they haven't spoken yet
        if requested:
            requested_speaker = self._speaker_by_name.get(requested)
            if requested_speaker and requested_speaker.name not in spoken:
                # Valid request - the requested person goes next
                return requested_speaker

        # Otherwise, pick random from those who haven't spoken (excluding current)
        available = [
            s
            for s in self.speakers
            if s.name not in spoken and s.name != current_speaker.name
        ]
        if not available:
            # Everyone has spoken (shouldn't happen in normal flow)
            return current_speaker

        return random.choice(available)

    def run(
        self, rounds: int | None = None, initial_history: ChatHistory | None = None
    ) -> ChatHistory:
        """
        Run the group conversation.

        Each round: all speakers speak once.
        Round 1: starts with random speaker.
        Subsequent rounds: starts with the requested speaker from previous round.
        Within a round: if someone requests a reply, that person goes next (if they haven't spoken yet).

        Args:
            rounds: Number of conversation rounds (uses config default if None)
            initial_history: Optional initial chat history to start with

        Returns:
            The complete chat history
        """
        rounds = rounds or CONVERSATION_ROUNDS
        chat_history: ChatHistory = initial_history.copy() if initial_history else []

        # Display initial state
        self.console.print(Markdown(self.format_conversation_display(chat_history)))

        # Round 1: start with random speaker
        requested_next = None

        for round_num in range(rounds):
            self.console.print(Markdown(f"\n## Ronda {round_num + 1}\n"))

            # Track who has spoken in this round
            spoken: set[str] = set()

            # Determine starting speaker for this round
            if requested_next:
                current_speaker = self._speaker_by_name.get(requested_next)
                if not current_speaker or requested_next in spoken:
                    # Invalid or already spoken, pick random
                    available = list(self.speakers)
                    current_speaker = random.choice(available)
            else:
                # Round 1: random start
                current_speaker = random.choice(self.speakers)

            # Each speaker speaks once per round
            while len(spoken) < len(self.speakers):
                # Current speaker speaks
                response = current_speaker.speak(chat_history)
                spoken.add(current_speaker.name)

                # Track who was requested for next round (only non-pets)
                if not current_speaker.config.is_pet:
                    requested_next = response.requesting_reply_from

                # If we haven't completed the round, get next speaker
                if len(spoken) < len(self.speakers):
                    # Determine next speaker based on request
                    current_speaker = self._get_next_speaker(
                        current_speaker, requested_next, spoken
                    )

            self.console.print(Markdown("\n---\n"))

        return chat_history
