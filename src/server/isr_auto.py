"""Auto-registration of ISR routes"""

from fastapi import APIRouter
from fastapi.routing import APIRoute

from .isr import ISRRoute, isr_registry


def auto_register_isr_routes(*routers: APIRouter):
    """
    Automatically register all ISR-decorated routes for pre-warming.
    Call this after all routes are defined.
    """
    routes_registered = 0

    for router in routers:
        for route in router.routes:
            if isinstance(route, APIRoute) and hasattr(route.endpoint, "_isr_template"):
                endpoint = route.endpoint

                # Create data fetcher that works without request
                def make_data_fetcher(handler, route_path):
                    async def fetcher(base_url: str, **params):
                        # Create a minimal mock request
                        class MockRequest:
                            class URL:
                                path = route_path

                            url = URL()
                            headers: dict = {}

                        return await handler(MockRequest(), base_url=base_url, **params)

                    return fetcher

                # Register the route
                data_fetcher = make_data_fetcher(endpoint._original_func, route.path)

                isr_registry.register(
                    ISRRoute(
                        path=route.path,
                        template=endpoint._isr_template,
                        ttl=endpoint._isr_ttl,
                        stale_while_revalidate=endpoint._isr_stale_while_revalidate,
                        data_fetcher=(
                            data_fetcher if not endpoint._isr_slug_fetcher else None
                        ),
                        slug_fetcher=endpoint._isr_slug_fetcher,
                        slug_data_fetcher=(
                            data_fetcher if endpoint._isr_slug_fetcher else None
                        ),
                    )
                )
                routes_registered += 1

    print(f"Auto-registered {routes_registered} ISR routes for pre-warming")
    return routes_registered
