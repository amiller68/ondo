from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse

from src.leaky import BlogPost
from ...deps import leaky_url
from ...handlers import ComponentResponseHandler, ISRHandler

router = APIRouter(prefix="/blog")


@router.get("/posts", response_class=HTMLResponse)
async def blog_posts(request: Request, base_url: str = Depends(leaky_url)):
    """API endpoint for blog posts list component"""
    isr_handler = ISRHandler(ttl=3600, stale_while_revalidate=60)
    handler = ComponentResponseHandler("components/blog/blog_posts_list.html")

    async def fetch_posts(base_url: str):
        posts = await BlogPost.read_all(base_url)
        return {"posts": posts}

    return await isr_handler.cached_response(
        request=request,
        fetch_func=fetch_posts,
        response_handler=handler,
        base_url=base_url,
    )


@router.get("/posts/{category}/{name}", response_class=HTMLResponse)
async def blog_post(
    request: Request, category: str, name: str, base_url: str = Depends(leaky_url)
):
    """API endpoint for single blog post component"""
    isr_handler = ISRHandler(ttl=3600, stale_while_revalidate=60)
    handler = ComponentResponseHandler("components/blog/blog_post.html")

    async def fetch_post(base_url: str, category: str, name: str):
        post = await BlogPost.read_one(base_url=base_url, name=f"{category}/{name}")

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return {
            "category": category,
            "name": name,
            "created_at": post.created_at,
            "title": post.title,
            "description": post.description,
            "content": post.content,
        }

    return await isr_handler.cached_response(
        request=request,
        fetch_func=fetch_post,
        response_handler=handler,
        base_url=base_url,
        category=category,
        name=name,
    )
