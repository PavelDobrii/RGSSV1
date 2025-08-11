from fastapi import APIRouter
import structlog

router = APIRouter(tags=["health"])
logger = structlog.get_logger()


@router.get("/healthz")
async def healthz():
    logger.info("healthz")
    return {"status": "ok"}


@router.get("/readyz")
async def readyz():
    logger.info("readyz")
    return {"status": "ready"}
