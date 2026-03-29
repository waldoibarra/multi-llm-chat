"""Main entry point for the 3-way LLM conversation."""

from src.config import CONVERSATION_ROUNDS, SPEAKERS
from src.llm_client import LLMClient
from src.orchestrator import ConversationOrchestrator
from src.speakers import Speaker


def main() -> None:
    # Initialize the LLM client
    llm_client = LLMClient()

    # Create speakers from config
    speakers = [
        Speaker(config=config, llm_client=llm_client) for config in SPEAKERS.values()
    ]

    # Create the orchestrator
    orchestrator = ConversationOrchestrator(speakers=speakers)

    # Run the conversation
    orchestrator.run(rounds=CONVERSATION_ROUNDS)


if __name__ == "__main__":
    main()
