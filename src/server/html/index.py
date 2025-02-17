from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.state import AppState
from ..deps import state
from . import gallery
from . import blog
from . import music

router = APIRouter()
router.include_router(gallery.router)
router.include_router(blog.router)
router.include_router(music.router)
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request, _state: AppState = Depends(state)):
    # TODO: re-implement hot reloading
    # NOTE: special carve out for serving index content back to the app
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("pages/index.html", {"request": request})
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("pages/about.html", {"request": request})
    return templates.TemplateResponse(
        "index.html", {"request": request, "page_content": "pages/about.html"}
    )
