"""
Defines the FastAPI routes for the MiniVault API. This module includes a
streaming endpoint (`/generate`) that accepts a prompt and streams the model's
response back token-by-token using a generator and FastAPI's StreamingResponse.

Each interaction is logged after completion for auditing or debugging purposes.
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.model import generate_tokens
from app.logger import log_interaction

router = APIRouter()


class Prompt(BaseModel):
    """
    Request model for the `/generate` endpoint.

    Attributes:
        prompt (str): The user-provided input string used to generate text.
    """
    prompt: str


@router.post("/generate", response_class=StreamingResponse, tags=["Generation"])
async def generate(prompt: Prompt):
    """
    Endpoint that streams text generation in real-time from a language model.

    This route receives a text prompt and returns a streaming text response,
    yielding one token at a time as it is generated. The full prompt-response
    interaction is logged after generation is complete.

    Args:
        prompt (Prompt): The JSON request body containing the input text.

    Returns:
        StreamingResponse: A streaming HTTP response that sends back generated tokens
        one-by-one as plain text.

    Example Request:
        POST /generate
        {
            "prompt": "Once upon a time"
        }

    Example Response (streamed text):
        " there was a curious little fox..."
    """
    prompt_text = prompt.prompt
    tokens = generate_tokens(prompt_text)

    def stream():
        full_output = ""
        for token in tokens:
            full_output += token
            yield token
        log_interaction(prompt_text, full_output)

    return StreamingResponse(stream(), media_type="text/plain")
