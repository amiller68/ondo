from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.leaky.models.tracks import AudioTrack
from src.leaky.models.listening import ListeningEntry
from ..deps import leaky_url

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/music", response_class=HTMLResponse)
async def music_index_page(
    request: Request, 
    category: str = "me",
    base_url: str = Depends(leaky_url)
):
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            "pages/music/index.html", 
            {"request": request, "category": category}
        )
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "page_content": "pages/music/index.html",
            "category": category
        }
    )


@router.get("/music/api/content", response_class=HTMLResponse)
async def music_content(
    request: Request, 
    category: str = "me",
    base_url: str = Depends(leaky_url)
):
    if category == "me":
        tracks = await AudioTrack.read_all(base_url)
        return templates.TemplateResponse(
            "components/music/tracks_list.html", 
            {"request": request, "tracks": tracks}
        )
    else:  # category == "listening"
        entries = await ListeningEntry.read_all(base_url)
        return templates.TemplateResponse(
            "components/music/listening_list.html", 
            {"request": request, "entries": entries}
        )


@router.get("/music/listening/{name}", response_class=HTMLResponse)
async def listening_page(request: Request, name: str):
    context = {"request": request, "name": name}
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("pages/music/listening.html", context)
    return templates.TemplateResponse(
        "index.html", {**context, "page_content": "pages/music/listening.html"}
    )


@router.get("/music/api/listening/{name}", response_class=HTMLResponse)
async def listening_entry(request: Request, name: str, base_url: str = Depends(leaky_url)):
    entry = await ListeningEntry.read_one(base_url=base_url, name=name)

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    context = {
        "request": request,
        "entry": entry,
    }
    return templates.TemplateResponse("components/music/listening_entry.html", context) 