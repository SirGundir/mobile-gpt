from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from api.utils import get_current_user
from api.services.searcher import Searcher

router = APIRouter(
    prefix="/search"
)

class SearchSchema(BaseModel):
    request: str
    region: Optional[str] = "ru-ru"
    max_results: Optional[int] = None

@router.post('')
async def route(schema: SearchSchema, token: str = Depends(get_current_user)):
    return {
        'status': 'ok',
        'results': await Searcher().search(schema.request, region=schema.region, max_results=schema.max_results)
    }
