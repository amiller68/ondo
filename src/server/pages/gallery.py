from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse

from src.leaky import GalleryImage
from ..deps import leaky_url
from ..handlers import PageResponse, ComponentResponseHandler

router = APIRouter()


@router.get("/gallery", response_class=HTMLResponse)
async def gallery_index_page(request: Request):
    """Gallery index page"""
    page = PageResponse("pages/gallery/index.html", layout="layouts/app.html")
    return page.render(request, {})


@router.get("/gallery/api/items", response_class=HTMLResponse)
async def gallery_items(request: Request, base_url: str = Depends(leaky_url)):
    """API endpoint for gallery items grid component"""
    images = await GalleryImage.read_all(base_url)
    handler = ComponentResponseHandler("components/gallery/gallery_items_grid.html")
    return await handler.respond(request, {"images": images})


@router.get("/gallery/{category}/{name}", response_class=HTMLResponse)
async def gallery_item_page(
    request: Request, category: str, name: str, base_url: str = Depends(leaky_url)
):
    """Gallery item detail page"""
    page = PageResponse("pages/gallery/item.html", layout="layouts/app.html")
    return page.render(request, {"category": category, "name": name})


@router.get("/gallery/api/items/{category}/{name}", response_class=HTMLResponse)
async def gallery_item(
    request: Request, category: str, name: str, base_url: str = Depends(leaky_url)
):
    """API endpoint for single gallery item component"""
    image = await GalleryImage.read_one(base_url, category, name)

    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    handler = ComponentResponseHandler("components/gallery/gallery_item.html")
    return await handler.respond(request, {"image": image})
