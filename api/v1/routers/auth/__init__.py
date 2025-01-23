from fastapi import APIRouter

from .login import router as router_login

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

routers = [router_login]
[router.include_router(_router) for _router in routers]
