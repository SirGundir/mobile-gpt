from fastapi import APIRouter, Depends
from typing import Optional
from pydantic import BaseModel

from api.utils import get_current_user
from api.services import OpenAIClient
from config import settings

router = APIRouter(
    prefix="/ask/advanced"
)

class AdvancedAskSchema(BaseModel):
    question: str
    from_lang: str = "ru"
    to_lang: str = "ru"
    context: Optional[str] = None
    model: str = settings.default_model

@router.post('')
async def route(schema: AdvancedAskSchema):
    return {
        'status': 'ok',
        'results': await OpenAIClient().advanced_ask(
            question=schema.question,
            from_lang=schema.from_lang,
            to_lang=schema.to_lang,
            context=schema.context,
            model=schema.model
        )
    }
