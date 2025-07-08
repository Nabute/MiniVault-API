"""
This is the entry point for the MiniVault API application.

It initializes a FastAPI application instance with metadata, loads model resources at startup,
and includes route definitions from the `app.routes` module.

Key Features:
- Loads and caches a local Hugging Face language model at startup.
- Exposes a RESTful interface using FastAPI.
- Modular architecture with route separation.
"""

from fastapi import FastAPI
from app import model
from app.routes import router

# Initialize FastAPI application with metadata
app = FastAPI(
    title="MiniVault API",
    description="A lightweight API for secure vault-like storage services.",
    version="1.0.0"
)

# Register routes
app.include_router(router)

@app.on_event("startup")
def startup_event() -> None:
    """
    FastAPI startup event handler.

    Ensures the model and tokenizer are downloaded and loaded into memory
    before serving any requests. This avoids repeated initialization
    and prepares the model for inference.
    """
    model.ensure_model_downloaded()
    model.load_model()
