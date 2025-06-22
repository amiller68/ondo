from fastapi import APIRouter

from . import cache

router = APIRouter(prefix="/v0")

router.include_router(cache.router)