from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ...cache import cache

router = APIRouter()


@router.get("/cache/stats")
async def cache_stats():
    """Get cache statistics"""
    stats = cache.get_stats()
    return JSONResponse(content=stats)


@router.post("/cache/invalidate")
async def invalidate_cache(pattern: Optional[str] = None):
    """Invalidate cache entries"""
    cache.invalidate(pattern)
    return JSONResponse(content={"status": "ok", "pattern": pattern})
