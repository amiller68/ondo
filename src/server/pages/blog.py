from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse

from src.leaky import BlogPost
from ..deps import leaky_url
from ..handlers import PageResponse, ComponentResponseHandler

router = APIRouter()


@router.get("/blog", response_class=HTMLResponse)
async def blog_index_page(request: Request, base_url: str = Depends(leaky_url)):
    """Blog index page"""
    page = PageResponse("pages/blog/index.html", layout="layouts/app.html")
    return page.render(request, {})


@router.get("/blog/api/posts", response_class=HTMLResponse)
async def blog_index_posts(request: Request, base_url: str = Depends(leaky_url)):
    """API endpoint for blog posts list component"""
    posts = await BlogPost.read_all(base_url)
    handler = ComponentResponseHandler("components/blog/blog_posts_list.html")
    return await handler.respond(request, {"posts": posts})


@router.get("/blog/{category}/{name}", response_class=HTMLResponse)
async def blog_post_page(request: Request, category: str, name: str):
    """Blog post detail page"""
    page = PageResponse("pages/blog/post.html", layout="layouts/app.html")
    return page.render(request, {"category": category, "name": name})


@router.get("/blog/api/posts/{category}/{name}", response_class=HTMLResponse)
async def blog_post(
    request: Request, category: str, name: str, base_url: str = Depends(leaky_url)
):
    """API endpoint for single blog post component"""
    post = await BlogPost.read_one(base_url=base_url, name=f"{category}/{name}")

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    context = {
        "category": category,
        "name": name,
        "created_at": post.created_at,
        "title": post.title,
        "description": post.description,
        "content": post.content,
    }
    handler = ComponentResponseHandler("components/blog/blog_post.html")
    return await handler.respond(request, context)
