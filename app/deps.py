from functools import lru_cache

from fastapi import Depends, Header, HTTPException, status

from .settings import settings
from .services.route_service import RouteService
from .services.tts_service import TTSService
from .services.map_service import MapService
from .integrations.content_ai import ContentAI
from .integrations.tts_provider import TTSProvider


async def get_settings():
    return settings


def api_key_auth(x_api_key: str | None = Header(default=None)):
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid api key")
    return x_api_key


def get_content_ai() -> ContentAI:
    return ContentAI()


def get_tts_provider() -> TTSProvider:
    return TTSProvider()


def get_map_service(settings=Depends(get_settings)) -> MapService:
    return MapService(api_key=settings.google_maps_api_key)


@lru_cache()
def get_tts_service() -> TTSService:
    """Return a single :class:`TTSService` instance for all requests."""

    provider = get_tts_provider()
    return TTSService(provider)


def get_route_service(
    content_ai: ContentAI = Depends(get_content_ai),
    map_service: MapService = Depends(get_map_service),
    tts_service: TTSService = Depends(get_tts_service),
) -> RouteService:
    return RouteService(content_ai, map_service, tts_service)
