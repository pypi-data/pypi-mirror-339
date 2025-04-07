import os

import requests


def get_openrouter_headers() -> dict[str, str]:
    """Get headers for OpenRouter API requests.

    Returns:
        Dict containing the required headers

    Raises:
        ValueError: If OPENROUTER_API_KEY environment variable is not set
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable must be set")

    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": os.getenv("HTTP_REFERER", "http://localhost:3000"),  # Required by OpenRouter
        "X-Title": os.getenv("X_TITLE", "Local Development"),  # Optional but recommended
    }


def list_models() -> list[dict[str, str]]:
    """List all available models from OpenRouter API.

    Returns:
        List of model information dictionaries containing details like id, name, context_length, etc.

    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    response = requests.get("https://openrouter.ai/api/v1/models", headers=get_openrouter_headers())
    response.raise_for_status()
    return list(response.json()["data"])
