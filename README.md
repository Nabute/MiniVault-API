# MiniVault API

MiniVault API is a small demonstration service built with [FastAPI](https://fastapi.tiangolo.com/). It exposes a single endpoint that **streams** text generated from a locally cached HuggingFace model. All interactions are logged in JSON Lines format for auditing and debugging purposes.

## Features

- **/generate endpoint** – Accepts a text prompt and streams tokens from a distilGPT2 model.
- **Logging** – Every request and response pair is appended to `logs/log.jsonl` with a UTC timestamp.
- **Easy to extend** – The codebase is intentionally lightweight so real AI logic can be plugged in later.

## Demo Video

> See the full walkthrough of the local model and streaming output in action:

[Watch Demo](https://www.loom.com/share/cc1509989aff4af18cf749b3d4e37ddb?sid=98e03b0a-2d8a-4d0b-a311-597efbb91fed)

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

## Model Download

The first time the server starts it will automatically download the model files
to `./models/distilgpt2`. Once downloaded the service can run fully offline
using the cached copy.

## API Usage

### `POST /generate`

Send a JSON body containing a `prompt` string. The server streams back tokens as they are generated.

Request example:
```bash
curl --no-buffer -X POST http://127.0.0.1:8000/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello"}'
```

Response example (streamed):
```
Hello there...
```

## Logging

All interactions are appended to [`logs/log.jsonl`](logs/log.jsonl). Each line is a JSON object with the following keys:

- `timestamp` – UTC timestamp of the request.
- `prompt` – The prompt received from the client.
- `response` – The text returned by the API.

Example log line:
```json
{"timestamp": "2025-07-08T10:23:45.123Z", "prompt": "Hello", "response": "Hi there!"}
```

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
├── models/
│   └── distilgpt2/
├── requirements.txt
└── README.md
```
