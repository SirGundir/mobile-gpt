from fastapi import APIRouter

from .routers.health import router as router_health

router = APIRouter(
    prefix="/v1",
    tags=["V1"]
)

routers = [router_health]
[router.include_router(_router) for _router in routers]
