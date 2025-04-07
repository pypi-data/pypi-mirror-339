import os
from typing import Optional

import requests


def get_groq_headers() -> dict[str, str]:
    """Get headers for Groq API requests.

    Returns:
        Dict containing the required headers

    Raises:
        ValueError: If GROQ_API_KEY environment variable is not set
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable must be set")

    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def list_models() -> list[str]:
    """List all available active models from Groq API.

    Returns:
        List of model IDs that are currently active

    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    response = requests.get("https://api.groq.com/openai/v1/models", headers=get_groq_headers())
    response.raise_for_status()
    data = response.json()

    # Filter for active models and return only their IDs
    return [model["id"] for model in data["data"] if model["active"]]


def create_completion(model: str, messages: list[dict[str, str]], temperature: float = 0.7, max_tokens: Optional[int] = None, stream: bool = False, **kwargs) -> dict:  # noqa: ANN003, ANN401
    """Create a chat completion using the Groq API.

    Args:
        model: The model to use (e.g., "mixtral-8x7b-32768")
        messages: List of message dictionaries with 'role' and 'content'
        temperature: Controls randomness in the response (0.0 to 1.0)
        max_tokens: Maximum number of tokens to generate
        stream: Whether to stream the response
        **kwargs: Additional parameters to pass to the API

    Returns:
        Dict containing the API response

    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    payload = {"model": model, "messages": messages, "temperature": temperature, "stream": stream, **kwargs}

    if max_tokens is not None:
        payload["max_tokens"] = max_tokens

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=get_groq_headers(), json=payload)
    response.raise_for_status()
    return response.json()
