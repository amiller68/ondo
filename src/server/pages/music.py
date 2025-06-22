from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from src.leaky.models.tracks import AudioTrack
from ..deps import leaky_url
from ..handlers import PageResponse, ComponentResponseHandler

router = APIRouter()


@router.get("/music", response_class=HTMLResponse)
async def music_index_page(request: Request):
    """Music index page"""
    page = PageResponse("pages/music/index.html", layout="layouts/app.html")
    return page.render(request, {})


@router.get("/music/api/content", response_class=HTMLResponse)
async def music_content(request: Request, base_url: str = Depends(leaky_url)):
    """API endpoint for music content component"""
    tracks = await AudioTrack.read_all(base_url)
    handler = ComponentResponseHandler("components/music/tracks_table.html")
    return await handler.respond(request, {"tracks": tracks})
