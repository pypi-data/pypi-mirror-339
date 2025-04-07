# qexec-ai

A Python package for executing commands through AI using qexec.

## Installation

```bash
pip install qexec-ai
```

## Usage

```python
from qexec_ai import configure, register_exec, call_llm

# Configure the AI
configure(
    model="your-model",
    api_key="your-api-key"
)

# Register a command
def my_function():
    print("Function executed!")

register_exec("my-command", my_function, description="Execute my function", type="button")

# Use the AI
reply = call_llm("Please execute my command")
parse_and_execute(reply)
```

## Features

- AI-powered command execution
- Support for button, switch, and range type commands
- Memory management for conversation history
- Secure encryption for stored data
