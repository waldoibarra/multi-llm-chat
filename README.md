# Multi-LLM Chat

A CLI tool that runs multi-party conversations between multiple LLMs, each with distinct speaker personalities.

![Example chat](/assets/example-chat.png)

## Overview

This project simulates a group conversation between 4 speakers with unique personalities:

- **K'inich** — Dog, eternal optimist, speaks in barks and sounds
- **Lluvia** — Woman, cosmiatra, sarcastic and witty
- **Waldo** — Man, philosopher and software architect
- **Axel** — kid, loves video games and anime, very logical

The conversation runs for multiple rounds, with each speaker responding to the chat history and optionally requesting a specific person to respond next.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) — Package manager

## Setup

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
   Get your API key from [https://console.groq.com/keys](https://console.groq.com/keys)

## Usage

Run the conversation:
```bash
uv run multi-llm
```

Or as a Python module:
```bash
uv run python -m src.main
```

## Development

### Code Quality Tools

This project uses several tools to maintain code quality:

```bash
# Linting
uv run ruff check src/

# Auto-fix linting issues
uv run ruff check src/ --fix

# Code formatting
uv run black src/

# Type checking
uv run mypy src/
```

### Pre-commit Hooks

The pre-commit hook is already installed. It runs ruff, black, and mypy on every commit to ensure code quality.

To run manually:
```bash
uv run pre-commit run --all-files
```

### Running Tests

No tests for this project as this is just a POC.

## Project Structure

```
.
├── src/
│   ├── __init__.py         # Package marker
│   ├── __main__.py         # Entry point for `python -m src`
│   ├── config.py           # Speaker configurations and prompts
│   ├── llm_client.py       # LLM API client (Groq/OpenAI compatible)
│   ├── main.py             # CLI entry point
│   ├── orchestrator.py     # Conversation flow management
│   └── speakers.py         # Speaker classes and responses
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Configuration

### Changing Speakers

Edit `src/config.py` to modify:

- Speaker names (`SPEAKER_NAMES`)
- Speaker models (`SPEAKER_MODELS`)
- Speaker colors for console display (`SPEAKER_COLORS`)
- System prompts (`_build_system_prompts()`)
- Conversation rounds (`CONVERSATION_ROUNDS`)
- Conversation goal (`CONVERSATION_GOAL`)
- Response constraints (`CONSTRAINTS_PROMPT`)

### Changing the Models per Participant

Update `DEFAULT_MODEL` in `src/config.py`:

```python
DEFAULT_MODEL = "openai/gpt-oss-20b"  # Groq model
```

Or set a different model per participant by modifying `SPEAKER_MODELS`.

> Available Groq models: `mixtral-8x7b-32768`, `llama-3.1-70b-versatile`, `gemma2-9b-it`, etc.

## Architecture

- **LLMClient** — Abstraction over OpenAI-compatible APIs (currently uses Groq)
- **Speaker** — Represents each participant with personality, model, and chat history
- **ConversationOrchestrator** — Manages conversation flow, rounds, and speaker selection

## License

MIT License — See [LICENSE](LICENSE) file.
