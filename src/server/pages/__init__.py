from fastapi import APIRouter

from . import index, gallery, blog, music
from ..isr_auto import auto_register_isr_routes

router = APIRouter()
router.include_router(index.router)
router.include_router(gallery.router)
router.include_router(blog.router)
router.include_router(music.router)

# Auto-register all ISR routes for pre-warming
auto_register_isr_routes(index.router, gallery.router, blog.router, music.router)
