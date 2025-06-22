from fastapi import APIRouter

from . import index, gallery, blog, music

router = APIRouter()
router.include_router(index.router)
router.include_router(gallery.router)
router.include_router(blog.router)
router.include_router(music.router)
