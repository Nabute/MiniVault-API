# MiniVault API - Stubbed API

MiniVault API is a small demonstration service built with [FastAPI](https://fastapi.tiangolo.com/). It exposes a single endpoint that returns a stubbed text response for a given prompt. All interactions are logged in JSON Lines format for auditing and debugging purposes.

## Features

- **/generate endpoint** – Accepts a text prompt and returns a stubbed response.
- **Logging** – Every request and response pair is appended to `logs/log.jsonl` with a UTC timestamp.
- **Easy to extend** – The codebase is intentionally lightweight so real AI logic can be plugged in later.

## Installation

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Python 3.10 or higher is recommended.

## Running the API

Start the development server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The service will be available at `http://127.0.0.1:8000`. FastAPI provides an interactive Swagger UI at `http://127.0.0.1:8000/docs`.

## API Usage

### `POST /generate`

Send a JSON body containing a `prompt` string. The server replies with a stubbed response.

Request example:
```bash
curl -X POST http://127.0.0.1:8000/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello"}'
```

Response example:
```json
{
  "response": "Stubbed response for: 'Hello'"
}
```

## Logging

All interactions are stored line by line in [`logs/log.jsonl`](logs/log.jsonl). Each line is a JSON object with the following keys:

- `timestamp` – UTC timestamp of the request.
- `prompt` – The prompt received from the client.
- `response` – The text returned by the API.

You can review this file to audit usage or debug issues.

## Project Structure

```
MiniVault-API/
├── app/
│   ├── logger.py   # Log helper
│   ├── main.py     # Application entry point
│   ├── model.py    # Placeholder response generator
│   └── routes.py   # API route definitions
├── logs/
│   └── log.jsonl   # Interaction log
├── requirements.txt
└── README.md
```
