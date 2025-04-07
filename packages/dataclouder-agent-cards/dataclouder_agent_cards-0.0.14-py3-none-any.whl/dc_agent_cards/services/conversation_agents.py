import json
from typing import Optional

from pydantic import BaseModel
from pydantic_ai import Agent

from ..models.conversation_models import LangCodeDescription, TranslateDTO, TranslationDTO

# from dc_agent_cards.agents.pydantic_ai_utils import get_model
# from dc_agent_cards.conversation_models import LangCodeDescription
from .pydantic_agent_service import get_model


class CharacterCardData(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    scenario: Optional[str] = None
    first_mes: Optional[str] = None
    creator_notes: Optional[str] = None
    mes_example: Optional[str] = None
    alternate_greetings: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    system_prompt: Optional[str] = None
    post_history_instructions: Optional[str] = None
    character_version: Optional[str] = None
    # extensions: Optional[Dict[str, Any]] = None
    appearance: Optional[str] = None


# NOTE: es mi primer agente, funciona pero creo que debería aprender a optimizarlo.
async def translate_convenversation_card(conversation_card: dict, current_lang: str, target_lang: str) -> CharacterCardData:
    print(" ----> ", conversation_card)
    current_data = json.dumps(conversation_card)

    current_lang_description = LangCodeDescription.get(current_lang)
    print(" ----> ", current_lang_description)
    target_lang_description = LangCodeDescription.get(target_lang)

    conv_translator_agent = Agent(
        "gemini-1.5-flash",
        result_type=CharacterCardData,
        system_prompt="This is a character card for role playing, translate all the properties the best you can to the target language",
    )
    result = await conv_translator_agent.run(f"translate the character card to {target_lang_description}: " + current_data)

    return result


async def translate_text(translate_dto: TranslateDTO) -> TranslationDTO:
    instructions = f'The next text is in {translate_dto.target_lang}: "{translate_dto.text}". you most translate the best you can to {translate_dto.target_lang}'
    print(" ----> ", instructions)
    try:
        model = get_model("groq")

        translator_agent = Agent(
            model,
            result_type=TranslationDTO,
            system_prompt="Translate the text to the specified language, give me just one result, the most close translation to the original text",
        )
        result = await translator_agent.run(instructions)
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
