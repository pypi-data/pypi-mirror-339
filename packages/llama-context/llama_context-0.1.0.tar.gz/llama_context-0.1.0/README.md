# llama-context

[![PyPI version](https://img.shields.io/pypi/v/llama_context.svg)](https://pypi.org/project/llama_context/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-context)](https://github.com/llamasearchai/llama-context/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_context.svg)](https://pypi.org/project/llama_context/)
[![CI Status](https://github.com/llamasearchai/llama-context/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-context/actions/workflows/llamasearchai_ci.yml)

**Llama Context (llama-context)** is a toolkit within the LlamaSearch AI ecosystem designed for managing context in applications, particularly conversational AI or systems requiring state persistence. It likely handles storing, retrieving, and utilizing contextual information (like conversation history, user state, or session data) to inform application behavior.

## Key Features

- **Context Management:** Core logic for storing, updating, and retrieving context (`main.py`, `core.py`).
- **Session Tracking:** Potential support for managing context across user sessions.
- **History Management:** Specifically handling conversational history or sequences of events.
- **Contextualization:** Using stored context to influence downstream tasks (e.g., LLM prompts, recommendations).
- **Storage Backends (Potential):** May support different storage mechanisms for context (memory, DB, file).
- **Configurable:** Allows defining context window size, storage options, expiration policies, etc. (`config.py`).

## Installation

```bash
pip install llama-context
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-context.git
```

## Usage

*(Usage examples demonstrating how to store, retrieve, and use context will be added here.)*

```python
# Placeholder for Python client usage
# from llama_context import ContextManager, ContextConfig

# config = ContextConfig.load("config.yaml")
# context_manager = ContextManager(config)

# session_id = "user123_sessionABC"

# # Add items to context
# context_manager.add_entry(session_id, {"role": "user", "content": "Hello there!"})
# context_manager.add_entry(session_id, {"role": "assistant", "content": "Hi! How can I help?"})

# # Retrieve context
# current_context = context_manager.get_context(session_id, max_length=10)
# print(current_context)

# # Use context (e.g., for an LLM prompt)
# # prompt = build_prompt_with_context(current_context, new_user_query="Tell me a joke")
# # llm_response = llm.generate(prompt)
# # context_manager.add_entry(session_id, {"role": "user", "content": "Tell me a joke"})
# # context_manager.add_entry(session_id, {"role": "assistant", "content": llm_response})
```

## Architecture Overview

```mermaid
graph TD
    A[Application / Service] --> B{Context Manager (main.py, core.py)};
    B -- Read/Write --> C[(Context Store (Memory, DB, File))];
    A -- Request Context --> B;
    B -- Returns Context --> A;
    A -- Add Context Entry --> B;

    D[Configuration (config.py)] -- Configures --> B;
    D -- Configures --> C;

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:1px
```

1.  **Interaction:** An application interacts with the Context Manager to store or retrieve contextual information (e.g., for a specific user or session).
2.  **Context Manager:** Handles the logic for adding new entries, retrieving relevant context (potentially based on size limits or relevance), and managing the context lifecycle.
3.  **Context Store:** The actual storage backend where contextual data is persisted (e.g., in-memory dictionary, Redis, database).
4.  **Configuration:** Defines storage backend details, context window size, expiration rules, etc.

## Configuration

*(Details on configuring context storage backend (type, connection details), context length limits, expiration policies, session management, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-context.git
cd llama-context

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

### Testing

```bash
pytest tests/
```

### Contributing

Contributions are welcome! Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) and submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
