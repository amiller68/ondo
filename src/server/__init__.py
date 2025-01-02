from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles
from src.state import AppState
from .html import router as html_router
from .status import router as status_router


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

    templates = Jinja2Templates(directory="templates")

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
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "page_content": "pages/404.html"},
                status_code=404,
            )

        # For other errors, still return JSON
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    # Add middleware
    app.middleware("http")(state_middleware)
    app.middleware("http")(span_middleware)

    # TODO: hot reloading
    # if state.config.dev_mode:
    #     dev_router = APIRouter()
    #     @dev_router.get("/dev/reload")
    #     async def reload_html():

    #         async def event_generator():
    #             template_dir = Path("templates")
    #             try:
    #                 watcher = awatch(template_dir)
    #                 async for changes in watcher:
    #                     if changes:
    #                         yield {
    #                             "event": "reload",
    #                             "data": "reload"
    #                         }
    #             except asyncio.CancelledError:
    #                 print("Generator cancelled")
    #                 raise
    #             finally:
    #                 print("Generator cleanup")

    #         return EventSourceResponse(
    #             event_generator(),
    #             background=BackgroundTask(lambda: print("Connection closed")),
    #         )

    #     app.include_router(dev_router)

    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Include the HTML router
    app.include_router(html_router)
    app.include_router(status_router, prefix="/_status")

    return app


# This instance is used by uvicorn
app = None
