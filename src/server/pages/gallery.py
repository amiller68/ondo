from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse

from src.leaky import GalleryImage
from ..deps import leaky_url
from ..handlers import isr_page

router = APIRouter()


# Slug fetcher for dynamic routes
async def get_gallery_slugs(base_url: str):
    """Get all gallery item slugs for pre-warming"""
    images = await GalleryImage.read_all(base_url)
    slugs = []
    for image in images:
        if hasattr(image, "category") and hasattr(image, "name"):
            slugs.append({"category": image.category, "name": image.name})
        elif hasattr(image, "path"):
            parts = image.path.strip("/").split("/")
            if len(parts) >= 2:
                slugs.append({"category": parts[0], "name": parts[1]})
    return slugs


@router.get("/gallery", response_class=HTMLResponse)
@isr_page(template="pages/gallery/index.html", ttl=3600)
async def gallery_index_page(request: Request, base_url: str = Depends(leaky_url)):
    """Gallery index page with server-side rendered items"""
    images = await GalleryImage.read_all(base_url)
    return {"images": images}


@router.get("/gallery/{category}/{name}", response_class=HTMLResponse)
@isr_page(template="pages/gallery/item.html", ttl=3600, slug_fetcher=get_gallery_slugs)
async def gallery_item_page(
    request: Request, category: str, name: str, base_url: str = Depends(leaky_url)
):
    """Gallery item detail page with server-side rendered content"""
    image = await GalleryImage.read_one(base_url, category, name)

    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    return {
        "image": image,
        "category": category,
        "name": name,
    }
