from typing import Callable, List, Dict, Any, Optional
import asyncio
from dataclasses import dataclass

from fastapi.templating import Jinja2Templates

from .cache import cache

templates = Jinja2Templates(directory="templates")


@dataclass
class ISRRoute:
    """Configuration for an ISR-cached route"""

    path: str
    template: str
    ttl: int = 3600
    stale_while_revalidate: int = 60
    cache_key_prefix: Optional[str] = None

    # For static routes (like /blog)
    data_fetcher: Optional[Callable] = None

    # For dynamic routes (like /blog/:category/:name)
    slug_fetcher: Optional[Callable] = None
    slug_data_fetcher: Optional[Callable] = None


class ISRRegistry:
    """Registry for ISR routes that can be pre-warmed"""

    def __init__(self):
        self._routes: List[ISRRoute] = []

    def register(self, route: ISRRoute):
        """Register a route for ISR caching"""
        self._routes.append(route)
        return route

    async def prewarm_all(self, base_url: str):
        """Pre-warm all registered routes"""
        tasks = []

        for route in self._routes:
            if route.slug_fetcher:
                # Dynamic route - fetch all slugs then pre-warm each
                try:
                    slugs = await route.slug_fetcher(base_url)
                    for slug in slugs:
                        task = self._prewarm_route(base_url, route, slug)
                        tasks.append(task)
                except Exception as e:
                    print(f"Error fetching slugs for {route.path}: {e}")
            else:
                # Static route - pre-warm directly
                task = self._prewarm_route(base_url, route)
                tasks.append(task)

        # Execute all pre-warming tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Report results
        successful = sum(1 for r in results if not isinstance(r, Exception))
        failed = len(results) - successful

        print(f"✓ ISR pre-warming complete: {successful} pages cached")
        if failed > 0:
            print(f"✗ {failed} pages failed to cache")
            for result in results:
                if isinstance(result, Exception):
                    print(f"  - {result}")

        return successful, failed

    async def _prewarm_route(
        self, base_url: str, route: ISRRoute, slug: Optional[Dict[str, Any]] = None
    ):
        """Pre-warm a single route"""
        try:
            # Generate cache key
            if slug:
                # Dynamic route - format path with slug values
                path = route.path
                for key, value in slug.items():
                    path = path.replace(f"{{{key}}}", str(value))
                cache_key = f"{route.cache_key_prefix or 'isr'}:{path}"

                # Fetch data using slug
                if not route.slug_data_fetcher:
                    raise ValueError(
                        f"Missing slug_data_fetcher for route {route.path}"
                    )
                data = await route.slug_data_fetcher(base_url, **slug)
            else:
                # Static route
                cache_key = f"{route.cache_key_prefix or 'isr'}:{route.path}"

                # Fetch data
                if not route.data_fetcher:
                    raise ValueError(f"Missing data_fetcher for route {route.path}")
                data = await route.data_fetcher(base_url)

            # Check if already cached
            existing, _ = await cache.get(cache_key)
            if existing:
                return f"Already cached: {cache_key}"

            # Render template with data
            template_data = {"request": None, **data}  # No request during pre-warming
            content_template = templates.get_template(route.template)
            content_html = content_template.render(template_data)

            # Cache the rendered content
            cache.set(cache_key, content_html, ttl=route.ttl)

            return f"Pre-warmed: {cache_key}"

        except Exception as e:
            path = route.path
            if slug:
                for key, value in slug.items():
                    path = path.replace(f"{{{key}}}", str(value))
            return Exception(f"Failed to pre-warm {path}: {str(e)}")


# Global registry
isr_registry = ISRRegistry()
