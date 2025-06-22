from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from src.leaky.models.tracks import AudioTrack
from ..deps import leaky_url
from ..handlers import isr_page

router = APIRouter()


@router.get("/music", response_class=HTMLResponse)
@isr_page(template="pages/music/index.html", ttl=3600)
async def music_index_page(request: Request, base_url: str = Depends(leaky_url)):
    """Music index page with server-side rendered tracks"""
    tracks = await AudioTrack.read_all(base_url)
    return {"tracks": tracks}
