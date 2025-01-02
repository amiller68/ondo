from fastapi import APIRouter, Depends, HTTPException

from src.logger import RequestSpan
from src.server.deps import span

router = APIRouter()


@router.get("/healthz")
async def health(
    span: RequestSpan = Depends(span),
):
    try:
        return {"status": "ok"}
    except Exception as e:
        span.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
