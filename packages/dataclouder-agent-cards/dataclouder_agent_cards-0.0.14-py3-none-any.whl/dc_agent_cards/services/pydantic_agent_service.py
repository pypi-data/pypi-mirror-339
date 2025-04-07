import os

from pydantic_ai.models.anthropic import LatestAnthropicModelNames
from pydantic_ai.models.gemini import LatestGeminiModelNames
from pydantic_ai.models.openai import ChatModel, OpenAIModel

from ..controllers.open_router import list_models as list_openrouter_models
from ..models.conversation_models import ListModelsResponse, LLMProvider
from .groq_utils import list_models

DEFAULT_MODELS: dict[str, str] = {
    "openai": "o1-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "groq": "gemma2-9b-it",
    "google-gla": "gemini-2.0-flash-lite-preview-02-05",
    "google": "gemini-2.0-flash-lite-preview-02-05",  # support for both names
    "openrouter": "gryphe/mythomax-l2-13b:free",
}


def get_model(provider: str, model: str | None = None) -> str:
    if provider not in DEFAULT_MODELS:
        raise ValueError(f"Provider {provider} not supported")
    if provider == "google":
        provider = "google-gla"  # google generative language api
    elif provider == "openrouter":
        model = model or DEFAULT_MODELS[provider]
        return OpenAIModel(model, base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

    model = model or DEFAULT_MODELS[provider]
    return f"{provider}:{model}"


def get_model_names(provider: LLMProvider) -> list[ListModelsResponse]:
    if provider == LLMProvider.OpenAI:
        names = ChatModel.__args__
        return [ListModelsResponse(name=name, id=name) for name in names]
    elif provider == LLMProvider.Google:
        # models = genai.list_models()
        # gemini_models = [{**model.__dict__, 'id': model.name} for model in models if 'gemini' in model.name.lower()]
        # return  gemini_models
        names = LatestGeminiModelNames.__args__
        return [ListModelsResponse(name=name, id=name) for name in names]
    elif provider == LLMProvider.OpenRouter:
        models = list_openrouter_models()
        return models
    elif provider == LLMProvider.Groq:
        models = list_models()
        return [ListModelsResponse(name=name, id=name) for name in models]
    elif provider == LLMProvider.Anthropic:
        names = LatestAnthropicModelNames.__args__
        return [ListModelsResponse(name=name, id=name) for name in names]
    else:
        raise ValueError(f"Provider {provider} not supported")
