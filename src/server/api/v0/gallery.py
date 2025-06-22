from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse

from src.leaky import GalleryImage
from ...deps import leaky_url
from ...handlers import ComponentResponseHandler, ISRHandler

router = APIRouter(prefix="/gallery")


@router.get("/items", response_class=HTMLResponse)
async def gallery_items(request: Request, base_url: str = Depends(leaky_url)):
    """API endpoint for gallery items grid component"""
    isr_handler = ISRHandler(ttl=3600, stale_while_revalidate=60)
    handler = ComponentResponseHandler("components/gallery/gallery_items_grid.html")

    async def fetch_images(base_url: str):
        images = await GalleryImage.read_all(base_url)
        return {"images": images}

    return await isr_handler.cached_response(
        request=request,
        fetch_func=fetch_images,
        response_handler=handler,
        base_url=base_url,
    )


@router.get("/items/{category}/{name}", response_class=HTMLResponse)
async def gallery_item(
    request: Request, category: str, name: str, base_url: str = Depends(leaky_url)
):
    """API endpoint for single gallery item component"""
    isr_handler = ISRHandler(ttl=3600, stale_while_revalidate=60)
    handler = ComponentResponseHandler("components/gallery/gallery_item.html")

    async def fetch_image(base_url: str, category: str, name: str):
        image = await GalleryImage.read_one(base_url, category, name)

        if image is None:
            raise HTTPException(status_code=404, detail="Image not found")

        return {"image": image}

    return await isr_handler.cached_response(
        request=request,
        fetch_func=fetch_image,
        response_handler=handler,
        base_url=base_url,
        category=category,
        name=name,
    )
