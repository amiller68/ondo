from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse

from src.leaky import BlogPost
from ..deps import leaky_url
from ..handlers import isr_page

router = APIRouter()


# Slug fetcher for dynamic routes
async def get_blog_slugs(base_url: str):
    """Get all blog post slugs for pre-warming"""
    posts = await BlogPost.read_all(base_url)
    return [{"category": post.category, "name": post.name} for post in posts]


@router.get("/blog", response_class=HTMLResponse)
@isr_page(template="pages/blog/index.html", ttl=3600)
async def blog_index_page(request: Request, base_url: str = Depends(leaky_url)):
    """Blog index page with server-side rendered posts"""
    posts = await BlogPost.read_all(base_url)
    return {"posts": posts}


@router.get("/blog/{category}/{name}", response_class=HTMLResponse)
@isr_page(template="pages/blog/post.html", ttl=3600, slug_fetcher=get_blog_slugs)
async def blog_post_page(
    request: Request, category: str, name: str, base_url: str = Depends(leaky_url)
):
    """Blog post detail page with server-side rendered content"""
    post = await BlogPost.read_one(base_url=base_url, name=f"{category}/{name}")

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "category": category,
        "name": name,
    }
