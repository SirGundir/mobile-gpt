from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.utils import generate_token
from config import settings

router = APIRouter(
    prefix="/login"
)

class AuthSchema(BaseModel):
    username: str
    password: str

@router.post('')
async def route(schema: AuthSchema):
    if schema.password != settings.password:
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )
    return {
        'status': 'ok',
        'token': generate_token(schema.username)
    }
