from dataclouder_core.exception import handler_exception
from dc_agent_cards.models.conversation_models import ChatMessage
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic_ai import Agent
from pydantic_ai.messages import ModelRequest, ModelResponse, SystemPromptPart, TextPart, UserPromptPart
from pydantic_ai.models.anthropic import LatestAnthropicModelNames
from pydantic_ai.models.gemini import LatestGeminiModelNames
from pydantic_ai.models.openai import ChatModel

from ..models.conversation_models import ChatResponseDTO, ChatRole, ConversationMessagesDTO, ListModelsResponse, LLMProvider, TranslateDTO
from ..services import conversation_agents
from ..services.groq_utils import list_models
from ..services.pydantic_agent_service import get_model
from .open_router import list_models as list_openrouter_models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(prefix="/api/conversation/agent", tags=["Conversation Agents"])


@router.get("/test_error")
@handler_exception
async def test_error() -> None:
    raise Exception("test error")


@router.get("/list_models")
@handler_exception
async def get_model_names(provider: LLMProvider) -> list[ListModelsResponse]:
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


@router.post("/chat")
@handler_exception
async def chat(conversation_messages_dto: ConversationMessagesDTO) -> ChatResponseDTO:
    print(conversation_messages_dto)
    provider: str = conversation_messages_dto.model.provider or "groq"
    model_name: str | None = conversation_messages_dto.model.modelName or None
    model: str = get_model(provider, model_name)
    # Extract system messages and combine them into a single prompt
    system_messages = [msg.content for msg in conversation_messages_dto.messages or [] if msg.role == "system"]
    system_prompt = "\n".join(system_messages) if system_messages else "You are a helpful assistant."

    # Create agent with system prompt
    agent = Agent(model, system_prompt=system_prompt)

    # Get the last user message or use a default
    user_messages: list[ChatMessage] = [msg for msg in conversation_messages_dto.messages or [] if msg.role == "user"]
    user_prompt: str = user_messages[-1].content if user_messages else "Hello"

    # Convert messages to proper ModelMessage format
    message_history = []
    for msg in (conversation_messages_dto.messages or [])[:-1]:  # Exclude last user message
        if msg.role == "system":
            message_history.append(ModelRequest(parts=[SystemPromptPart(content=msg.content)]))
        elif msg.role == "user":
            message_history.append(ModelRequest(parts=[UserPromptPart(content=msg.content)]))
        elif msg.role == "assistant":
            message_history.append(ModelResponse(parts=[TextPart(content=msg.content)]))
    # What i can see this version create the whole conversation like chatgpt, so not sure if i'm adding more value.

    # Run the agent with history if available
    if message_history:
        result = await agent.run(user_prompt, message_history=message_history)
    else:
        result = await agent.run(user_prompt)

    return ChatResponseDTO(role=ChatRole.Assistant, content=result.data, metadata={"model": model})


@router.post("/translate_text")
async def translate_text(translate_dto: TranslateDTO) -> TranslateDTO:
    result = await conversation_agents.translate_text(translate_dto)
    print(result.data)
    return result.data


@router.post("/translate_card")
async def translate_card(card: dict) -> dict:
    result = await conversation_agents.translate_convenversation_card(card)
    print(result.data)
    return result.data
