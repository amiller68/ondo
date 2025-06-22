from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from src.state import AppState
from ..deps import state
from ..handlers import PageResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request, _state: AppState = Depends(state)):
    """Home page"""
    page = PageResponse("pages/index.html", layout="layouts/app.html")
    return page.render(request, {})


@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    """About page"""
    page = PageResponse("pages/about.html", layout="layouts/app.html")
    return page.render(request, {})
