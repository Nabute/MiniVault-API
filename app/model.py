"""
This module handles loading and inference for a local instance of a Hugging Face
causal language model (e.g., distilGPT2). It ensures the model and tokenizer are 
downloaded locally (for offline use), and provides a token-by-token generator 
for generating text with repetition penalty.

Features:
- Ensures local model availability
- Lazy model/tokenizer loading
- Greedy decoding with repetition penalty
"""

import torch
from pathlib import Path
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    RepetitionPenaltyLogitsProcessor,
    LogitsProcessorList,
)

# Model configuration
MODEL_NAME = "distilgpt2"
MODEL_DIR = Path("./models") / MODEL_NAME

# Global tokenizer and model instance (loaded lazily)
tokenizer = None
model = None


def ensure_model_downloaded():
    """
    Ensures the model and tokenizer are available in the local file system.

    If the local model directory or required tokenizer files are missing,
    this function downloads the model/tokenizer from Hugging Face Hub
    and saves them for offline use.
    """
    if not MODEL_DIR.exists() or not (MODEL_DIR / "tokenizer_config.json").exists():
        print(f"[Startup] Downloading and saving model {MODEL_NAME} to {MODEL_DIR}")
        # Download from Hugging Face hub
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

        # Save to local directory
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        _tokenizer.save_pretrained(str(MODEL_DIR))
        _model.save_pretrained(str(MODEL_DIR))


def load_model():
    """
    Loads the model and tokenizer from the local model directory.

    This function should be called once at startup to initialize the
    model and tokenizer. Sets them as global variables for reuse.
    """
    global tokenizer, model
    print("[Startup] Loading model/tokenizer from local files...")
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
    model = AutoModelForCausalLM.from_pretrained(str(MODEL_DIR))
    model.eval()
    print("[Startup] Model and tokenizer loaded.")


@torch.no_grad()
def generate_tokens(prompt: str, max_new_tokens: int = 50):
    """
    Generates tokens from the model one at a time using greedy decoding,
    with repetition penalty applied to reduce repetitive loops.

    Args:
        prompt (str): The input prompt to condition the generation.
        max_new_tokens (int): The maximum number of tokens to generate.

    Yields:
        str: The next decoded token in the generated sequence.

    Example:
        >>> for token in generate_tokens("The future of AI"):
        ...     print(token, end="")
    """
    # Encode the prompt into input tensor
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = input_ids

    # Set up repetition penalty processor
    repetition_penalty = 1.2
    logits_processor = LogitsProcessorList([
        RepetitionPenaltyLogitsProcessor(penalty=repetition_penalty)
    ])

    for _ in range(max_new_tokens):
        # Forward pass to get logits
        outputs = model(output_ids)
        logits = outputs.logits[:, -1, :]  # Last token logits

        # Apply repetition penalty
        logits = logits_processor(output_ids, logits)

        # Select the next token (greedy)
        next_token_id = torch.argmax(logits, dim=-1).unsqueeze(0)

        # Append to the output sequence
        output_ids = torch.cat([output_ids, next_token_id], dim=1)

        # Decode and yield the new token
        token = tokenizer.decode(next_token_id[0])
        yield token

        # Stop if EOS (end-of-sequence) token is generated
        if tokenizer.eos_token_id is not None and next_token_id.item() == tokenizer.eos_token_id:
            break
