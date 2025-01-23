from fastapi import APIRouter

from .search import router as router_search

router = APIRouter(
    prefix="/net",
    tags=["Internet"]
)

routers = [router_search]
[router.include_router(_router) for _router in routers]
