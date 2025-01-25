from fastapi import APIRouter

from .simple_ask import router as router_simple_ask

router = APIRouter(
    prefix="/llm",
    tags=["LLM"]
)

routers = [router_simple_ask]
[router.include_router(_router) for _router in routers]
