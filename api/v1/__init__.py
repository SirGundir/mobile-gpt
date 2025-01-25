from fastapi import APIRouter

from .routers.health import router as router_health
from .routers.auth import router as router_auth
from .routers.net import router as router_net
from .routers.llm import router as router_llm

router = APIRouter(
    prefix="/v1",
    tags=["V1"]
)

routers = [router_health, router_auth, router_net, router_llm]
[router.include_router(_router) for _router in routers]
