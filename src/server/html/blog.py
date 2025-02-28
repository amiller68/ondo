from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.leaky import BlogPost
from ..deps import leaky_url

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/blog", response_class=HTMLResponse)
async def blog_index_page(
    request: Request, category: str = "thoughts", base_url: str = Depends(leaky_url)
):
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            "pages/blog/index.html", {"request": request, "category": category}
        )
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page_content": "pages/blog/index.html",
            "category": category,
        },
    )


@router.get("/blog/api/posts", response_class=HTMLResponse)
async def blog_index_posts(
    request: Request, category: str = "thoughts", base_url: str = Depends(leaky_url)
):
    posts = await BlogPost.read_all(base_url, category=category)
    return templates.TemplateResponse(
        "components/blog/blog_posts_list.html", {"request": request, "posts": posts}
    )


@router.get("/blog/{category}/{name}", response_class=HTMLResponse)
async def blog_post_page(request: Request, category: str, name: str):
    context = {"request": request, "category": category, "name": name}

    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("pages/blog/post.html", context)
    return templates.TemplateResponse(
        "index.html", {**context, "page_content": "pages/blog/post.html"}
    )


@router.get("/blog/api/posts/{category}/{name}", response_class=HTMLResponse)
async def blog_post(
    request: Request, category: str, name: str, base_url: str = Depends(leaky_url)
):
    post = await BlogPost.read_one(base_url=base_url, name=f"{category}/{name}")

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    context = {
        "request": request,
        "category": category,
        "name": name,
        "created_at": post.created_at,
        "title": post.title,
        "description": post.description,
        "content": post.content,
    }
    return templates.TemplateResponse("components/blog/blog_post.html", context)
