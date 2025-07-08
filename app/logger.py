"""
logger.py

This module handles logging of prompt-response interactions in JSON Lines (JSONL) format.
Each log entry includes a UTC timestamp, the prompt received, and the corresponding response.

Logs are stored in `logs/log.jsonl` and appended to with each interaction.
"""

import json
from datetime import datetime
from pathlib import Path

# Path to the log file
LOG_PATH = Path("logs/log.jsonl")

# Ensure the parent directory exists
LOG_PATH.parent.mkdir(exist_ok=True)


def log_interaction(prompt: str, response: str):
    """
    Append a prompt-response interaction to the log file in JSONL format.

    Each log entry includes:
        - timestamp (UTC ISO format)
        - prompt (str): the input from the user
        - response (str): the generated or returned output

    Args:
        prompt (str): The user input or request.
        response (str): The generated response associated with the prompt.

    Example:
        >>> log_interaction("Hello", "Hi there!")
        # Adds a JSON line like:
        # {"timestamp": "2025-07-08T10:23:45.123Z", "prompt": "Hello", "response": "Hi there!"}
    """
    with open(LOG_PATH, "a") as f:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": prompt,
            "response": response
        }
        f.write(json.dumps(log_entry) + "\n")
