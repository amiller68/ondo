import hashlib
import json
from functools import wraps
from typing import Callable, Optional, Union

from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from ..cache import cache
from .component import ComponentResponseHandler
from .page import PageResponse

templates = Jinja2Templates(directory="templates")


class ISRHandler:
    """Incremental Static Regeneration handler with cache invalidation"""

    def __init__(
        self,
        ttl: int = 3600,
        stale_while_revalidate: int = 60,
        cache_key_prefix: Optional[str] = None,
    ):
        self.ttl = ttl
        self.stale_while_revalidate = stale_while_revalidate
        self.cache_key_prefix = cache_key_prefix or "isr"

    def _generate_cache_key(self, request: Request, **kwargs) -> str:
        """Generate cache key from request and parameters"""
        parts = [self.cache_key_prefix]

        # Add path
        parts.append(request.url.path)

        # Add query params
        if request.url.query:
            parts.append(request.url.query)

        # Add kwargs (route parameters)
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            parts.append(json.dumps(sorted_kwargs, sort_keys=True))

        # Add HTMX request header to differentiate partial/full responses
        if request.headers.get("HX-Request"):
            parts.append("htmx")

        # Create hash for complex keys
        key_str = ":".join(parts)
        if len(key_str) > 100:
            return (
                f"{self.cache_key_prefix}:{hashlib.md5(key_str.encode()).hexdigest()}"
            )

        return key_str

    async def cached_response(
        self,
        request: Request,
        fetch_func: Callable,
        response_handler: Optional[
            Union[PageResponse, ComponentResponseHandler]
        ] = None,
        **kwargs,
    ) -> Union[HTMLResponse, JSONResponse]:
        """
        Cache and return response with ISR pattern.

        Args:
            request: FastAPI request
            fetch_func: Async function that fetches the data
            response_handler: Optional handler for rendering response
            **kwargs: Additional parameters passed to fetch_func
        """
        # Check for cache invalidation based on root hash
        base_url = kwargs.get("base_url")
        if base_url:
            await cache.check_invalidation(base_url)

        # Generate cache key
        cache_key = self._generate_cache_key(request, **kwargs)

        # Try to get from cache
        async def fetch_and_render():
            # Fetch data
            data = await fetch_func(**kwargs)

            # If we have a response handler, render the response
            if response_handler:
                if isinstance(response_handler, PageResponse):
                    return response_handler.render(request, data)
                elif isinstance(response_handler, ComponentResponseHandler):
                    return await response_handler.respond(request, data)

            # Otherwise return raw data as JSON
            return JSONResponse(content=data)

        # Get from cache or fetch
        response, from_cache = await cache.get(
            cache_key,
            fetch_func=fetch_and_render,
            ttl=self.ttl,
            stale_while_revalidate=self.stale_while_revalidate,
        )

        # Add cache headers
        if isinstance(response, (HTMLResponse, JSONResponse)):
            response.headers["X-Cache"] = "HIT" if from_cache else "MISS"
            response.headers["Cache-Control"] = (
                f"public, max-age={self.ttl}, stale-while-revalidate={self.stale_while_revalidate}"
            )

        return response


def isr_cache(
    ttl: int = 3600,
    stale_while_revalidate: int = 60,
    cache_key_prefix: Optional[str] = None,
):
    """
    Decorator for ISR caching on route handlers.

    Usage:
        @router.get("/posts")
        @isr_cache(ttl=3600)
        async def get_posts(request: Request):
            posts = await fetch_posts()
            return {"posts": posts}
    """

    def decorator(func: Callable) -> Callable:
        handler = ISRHandler(ttl, stale_while_revalidate, cache_key_prefix)

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Extract function parameters
            func_kwargs = {**kwargs}
            if args:
                # Map positional args to kwargs based on function signature
                import inspect

                sig = inspect.signature(func)
                params = list(sig.parameters.keys())
                # Skip 'request' parameter
                if params and params[0] == "request":
                    params = params[1:]
                for i, arg in enumerate(args):
                    if i < len(params):
                        func_kwargs[params[i]] = arg

            async def fetch_func(**kw):
                # Call original function
                result = await func(request, **kw)
                return result

            # Return cached response
            return await handler.cached_response(request, fetch_func, **func_kwargs)

        return wrapper

    return decorator


def isr_page(
    template: str,
    layout: str = "layouts/app.html",
    ttl: int = 3600,
    stale_while_revalidate: int = 60,
    cache_key_prefix: Optional[str] = None,
    slug_fetcher: Optional[Callable] = None,
):
    """
    Decorator for ISR caching on page route handlers.
    Automatically registers routes for pre-warming.

    Usage:
        @router.get("/blog")
        @isr_page(template="pages/blog/index.html")
        async def blog_page(request: Request, base_url: str = Depends(leaky_url)):
            posts = await BlogPost.read_all(base_url)
            return {"posts": posts}

        # For dynamic routes with slugs:
        async def get_blog_slugs(base_url: str):
            posts = await BlogPost.read_all(base_url)
            return [{"category": p.category, "name": p.name} for p in posts]

        @router.get("/blog/{category}/{name}")
        @isr_page(template="pages/blog/post.html", slug_fetcher=get_blog_slugs)
        async def blog_post(request: Request, category: str, name: str, base_url: str = Depends(leaky_url)):
            ...
    """

    def decorator(func: Callable) -> Callable:
        handler = ISRHandler(ttl, stale_while_revalidate, cache_key_prefix)

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Generate cache key - don't include HX-Request header since we're only caching content
            cache_key = handler._generate_cache_key(request, **kwargs)
            # Remove htmx from cache key if present
            cache_key = cache_key.replace(":htmx", "")

            # Check for cache invalidation
            base_url = kwargs.get("base_url")
            if base_url:
                await cache.check_invalidation(base_url)

            # Get content HTML from cache or render
            async def fetch_and_render_content():
                # Get data from the route handler
                data = await func(request, *args, **kwargs)

                # Render just the content template
                template_data = {
                    "request": request,
                    **data,
                }
                content_template = templates.get_template(template)
                return content_template.render(template_data)

            content_html, from_cache = await cache.get(
                cache_key,
                fetch_func=fetch_and_render_content,
                ttl=handler.ttl,
                stale_while_revalidate=handler.stale_while_revalidate,
            )

            # Use PageResponse to handle the final rendering
            page = PageResponse(template, layout)
            response = page.render_with_content(request, content_html)

            # Add cache headers
            response.headers["X-Cache"] = "HIT" if from_cache else "MISS"
            response.headers["Cache-Control"] = (
                f"public, max-age={handler.ttl}, stale-while-revalidate={handler.stale_while_revalidate}"
            )

            return response

        # Store ISR config on wrapper for auto-registration
        setattr(wrapper, "_isr_template", template)
        setattr(wrapper, "_isr_ttl", ttl)
        setattr(wrapper, "_isr_stale_while_revalidate", stale_while_revalidate)
        setattr(wrapper, "_isr_slug_fetcher", slug_fetcher)
        setattr(wrapper, "_original_func", func)

        return wrapper

    return decorator
