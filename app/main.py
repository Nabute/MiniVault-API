"""
main.py

This is the entry point for the MiniVault API application.
It initializes a FastAPI app instance and includes application routes
from the `app.routes` module.

The API is built using FastAPI for fast and asynchronous HTTP interface support.
"""

from fastapi import FastAPI
from app.routes import router

# Initialize FastAPI application with metadata
app = FastAPI(
    title="MiniVault API",
    description="A lightweight API for secure vault-like storage services.",
    version="1.0.0"
)

# Include all route definitions from the routes module
app.include_router(router)
