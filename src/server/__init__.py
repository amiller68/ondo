from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from contextlib import asynccontextmanager
import asyncio
from pathlib import Path

from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse
from watchfiles import awatch
from src.state import AppState
from .pages import router as pages_router
from .api import router as api_router
from .health import router as health_router
from .status import router as status_router
from .handlers import PageResponse


def create_app(state: AppState) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await state.startup()
        yield
        await state.shutdown()

    async def state_middleware(request: Request, call_next):
        request.state.app_state = state
        return await call_next(request)

    async def span_middleware(request: Request, call_next):
        request.state.span = state.logger.get_request_span(request)
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            request.state.span.error(str(e))
            raise

    app = FastAPI(lifespan=lifespan)

    # Add exception handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        if request.headers.get("accept", "").startswith("application/json"):
            return JSONResponse(
                status_code=exc.status_code,
                content={"error": exc.detail},
            )

        print(f"HTTPException: {exc.status_code} {exc.detail}")
        # For HTML requests, render the 404 page
        if exc.status_code == 404:
            print("404")
            page = PageResponse("pages/404.html", layout="layouts/app.html")
            return page.render(request, {})

        # For other errors, still return JSON
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    # Add middleware
    app.middleware("http")(state_middleware)
    app.middleware("http")(span_middleware)

    # Hot reloading for development
    if state.config.dev_mode:
        dev_router = APIRouter()

        @dev_router.get("/dev/hot-reload")
        async def hot_reload():
            async def event_generator():
                template_dir = Path("templates")
                styles_dir = Path("styles")

                try:
                    # Watch both templates and styles directories
                    async for changes in awatch(template_dir, styles_dir):
                        if changes:
                            print(
                                f"Hot reload: detected changes in {[str(c[1]) for c in changes]}"
                            )
                            yield {"event": "reload", "data": "reload"}
                except asyncio.CancelledError:
                    print("Hot reload watcher cancelled")
                    raise
                except Exception as e:
                    print(f"Hot reload error: {e}")
                finally:
                    print("Hot reload cleanup")

            return EventSourceResponse(event_generator())

        app.include_router(dev_router)

    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Include routers
    app.include_router(pages_router)
    app.include_router(api_router)
    app.include_router(health_router)
    app.include_router(status_router, prefix="/_status")

    # and respond 200 to /up to please kamal
    @app.get("/up")
    async def up():
        return "OK"

    return app


# This instance is used by uvicorn
app = None
