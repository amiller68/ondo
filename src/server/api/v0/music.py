from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from src.leaky.models.tracks import AudioTrack
from ...deps import leaky_url
from ...handlers import ComponentResponseHandler, ISRHandler

router = APIRouter(prefix="/music")


@router.get("/content", response_class=HTMLResponse)
async def music_content(request: Request, base_url: str = Depends(leaky_url)):
    """API endpoint for music content component"""
    isr_handler = ISRHandler(ttl=3600, stale_while_revalidate=60)
    handler = ComponentResponseHandler("components/music/tracks_table.html")

    async def fetch_tracks(base_url: str):
        tracks = await AudioTrack.read_all(base_url)
        return {"tracks": tracks}

    return await isr_handler.cached_response(
        request=request,
        fetch_func=fetch_tracks,
        response_handler=handler,
        base_url=base_url,
    )
