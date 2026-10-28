from fastapi import APIRouter
from backend.app.api.feed import router as feed_router
from backend.app.api.item import router as item_router
from backend.app.api.trends import router as trends_router
from backend.app.api.search import router as search_router
from backend.app.api.health import router as health_router
from backend.app.api.domains import router as domains_router

api_router = APIRouter()
api_router.include_router(feed_router)
api_router.include_router(item_router)
api_router.include_router(trends_router)
api_router.include_router(search_router)
api_router.include_router(health_router)
api_router.include_router(domains_router)

__all__ = ["api_router"]
