from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.leaky import AudioTrack
from ..deps import leaky_url

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/audio", response_class=HTMLResponse)
async def audio_index_page(request: Request):
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("pages/audio/index.html", {"request": request})
    return templates.TemplateResponse(
        "index.html", {"request": request, "page_content": "pages/audio/index.html"}
    )


@router.get("/audio/api/tracks", response_class=HTMLResponse)
async def audio_tracks(request: Request, base_url: str = Depends(leaky_url)):
    tracks = await AudioTrack.read_all(base_url)
    return templates.TemplateResponse(
        "components/audio/audio_tracks_list.html", {"request": request, "tracks": tracks}
    )


@router.get("/audio/{name}", response_class=HTMLResponse)
async def audio_track_page(request: Request, name: str):
    context = {"request": request, "name": name}
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("pages/audio/track.html", context)
    return templates.TemplateResponse(
        "index.html", {**context, "page_content": "pages/audio/track.html"}
    )


@router.get("/audio/api/tracks/{name}", response_class=HTMLResponse)
async def audio_track(request: Request, name: str, base_url: str = Depends(leaky_url)):
    track = await AudioTrack.read_one(base_url=base_url, name=name)

    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    context = {
        "request": request,
        "track": track,
    }
    return templates.TemplateResponse("components/audio/audio_track.html", context) 