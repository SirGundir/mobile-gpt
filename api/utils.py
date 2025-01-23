import jwt
from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

def generate_token(username: str) -> str:
    """
    Генерация токена авторизации
    """
    return jwt.encode(
        {
            "user": username,
            "exp": datetime.now(tz=timezone.utc) + timedelta(days=7)
        },
        settings.jwt_secret,
        algorithm="HS256",
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Возвращает имя пользователя по токену
    """
    try:
        data = jwt.decode(token, settings.jwt_secret, algorithms='HS256')
        return data['username']
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=403,
            detail='Invalid token',
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=403,
            detail='Token expired',
        )
    except Exception:
        raise HTTPException(
            status_code=403,
            detail='Invalid token',
        )
