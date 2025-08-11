from fastapi import APIRouter, Depends, HTTPException, status
import structlog
from ..schemas import RouteGenerateRequest, RouteResponse
from ..deps import get_route_service, api_key_auth
from ..services.route_service import RouteService

router = APIRouter(prefix="/api/v1/routes", tags=["routes"])
logger = structlog.get_logger()


@router.post("/generate", response_model=RouteResponse)
async def generate_route(
    req: RouteGenerateRequest,
    service: RouteService = Depends(get_route_service),
    _: str = Depends(api_key_auth),
):
    logger.info("route.generate.start", city=req.city)
    try:
        route = await service.generate_route(
            city=req.city,
            start=(req.start.lat, req.start.lng) if req.start else None,
            duration_min=req.duration_min,
            transport_mode=req.transport_mode,
            interest_tags=req.interest_tags,
            language=req.language or "en",
            need_audio=req.need_audio,
        )
        logger.info("route.generate.success", route_id=route["route_id"], city=req.city)
        return RouteResponse(**route)
    except Exception as e:
        logger.exception("route.generate.error", city=req.city)
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=str(e))
