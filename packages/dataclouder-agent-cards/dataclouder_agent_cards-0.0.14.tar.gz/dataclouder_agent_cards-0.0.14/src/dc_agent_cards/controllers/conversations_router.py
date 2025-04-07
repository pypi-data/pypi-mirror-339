from datetime import datetime
from json import JSONEncoder

from bson import ObjectId

# from app.database.mongo import db
from dataclouder_core.db.mongo import db
from dc_agent_cards.models.conversation_models import TranslateCardDTO
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from notebooks.agents.conversation import CharacterCardData

from ..services import conversation_agents

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/api/conversation", tags=["Conversation Card AI"])


class MongoJSONEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:  # type: ignore # noqa: ANN401, F821
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


@router.post("/translate_card")
async def translate_conversation(
    request: TranslateCardDTO,
) -> CharacterCardData:
    # fb_admin.verify_token(token)
    conversation_card = db.get_collection("conversation_cards").find_one({"_id": ObjectId(request.idCard)})
    caracterData = conversation_card["characterCard"]["data"]
    print(caracterData)
    response = await conversation_agents.translate_convenversation_card(caracterData, request.currentLang, request.targetLang)
    print(response.data)
    return response.data
    # return {"status": "serving"}
