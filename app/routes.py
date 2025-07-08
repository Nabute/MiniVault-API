"""
routes.py

This module defines the API endpoints for the MiniVault service using FastAPI.
It includes a `/generate` endpoint that accepts a prompt and returns a stubbed response,
logging the interaction for auditing or debugging purposes.
"""

from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.model import generate_response
from app.logger import log_interaction

# Initialize a FastAPI router instance
router = APIRouter()


class Prompt(BaseModel):
    """
    Request model for the /generate endpoint.

    Attributes:
        prompt (str): The input string from the user to generate a response for.
    """
    prompt: str


@router.post("/generate", tags=["Generation"])
async def generate(prompt: Prompt, request: Request):
    """
    Generate a response for the given prompt.

    This endpoint accepts a user prompt, generates a stubbed response using the
    `generate_response` function, logs the interaction using `log_interaction`,
    and returns the response to the client.

    Args:
        prompt (Prompt): The request body containing the prompt string.
        request (Request): The FastAPI request object (useful for future enhancements like logging client IP).

    Returns:
        dict: A dictionary containing the generated response.

    Example Request:
        POST /generate
        {
            "prompt": "Hello"
        }

    Example Response:
        {
            "response": "Stubbed response for: 'Hello'"
        }
    """
    response_text = generate_response(prompt.prompt)
    log_interaction(prompt.prompt, response_text)
    return {"response": response_text}
