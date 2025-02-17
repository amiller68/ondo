from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.leaky import GalleryImage
from ..deps import leaky_url

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/gallery", response_class=HTMLResponse)
async def gallery_index_page(request: Request):
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            "pages/gallery/index.html", {"request": request}
        )
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page_content": "pages/gallery/index.html",
        },
    )


@router.get("/gallery/api/items", response_class=HTMLResponse)
async def gallery_items(request: Request, base_url: str = Depends(leaky_url)):
    images = await GalleryImage.read_all(base_url)
    return templates.TemplateResponse(
        "components/gallery/gallery_items_grid.html",
        {"request": request, "images": images},
    )


@router.get("/gallery/{category}/{name}", response_class=HTMLResponse)
async def gallery_item_page(
    request: Request, 
    category: str,
    name: str, 
    base_url: str = Depends(leaky_url)
):
    context = {
        "request": request,
        "category": category,
        "name": name,
    }
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("pages/gallery/item.html", context)
    return templates.TemplateResponse(
        "index.html", {**context, "page_content": "pages/gallery/item.html"}
    )


@router.get("/gallery/api/items/{category}/{name}", response_class=HTMLResponse)
async def gallery_item(
    request: Request, 
    category: str,
    name: str, 
    base_url: str = Depends(leaky_url)
):
    image = await GalleryImage.read_one(base_url, category, name)

    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")


    context = {
        "request": request,
        "image": image,
    }

    return templates.TemplateResponse("components/gallery/gallery_item.html", context)
