from ..integrations.tts_provider import TTSProvider
from ..utils.caching import get_cache
from ..settings import settings
import structlog


class TTSService:
    def __init__(self, provider: TTSProvider):
        self.provider = provider
        self.cache = get_cache()
        self.logger = structlog.get_logger(__name__)

    def cache_key(self, route_id: str, poi_id: str) -> str:
        return f"{route_id}:{poi_id}"

    def get_cached(self, route_id: str, poi_id: str) -> bytes | None:
        audio = self.cache.get(self.cache_key(route_id, poi_id))
        if audio:
            self.logger.info("tts.cache.hit", route_id=route_id, poi_id=poi_id)
        else:
            self.logger.info("tts.cache.miss", route_id=route_id, poi_id=poi_id)
        return audio

    def set_cached(self, route_id: str, poi_id: str, data: bytes) -> None:
        self.logger.info("tts.cache.set", route_id=route_id, poi_id=poi_id)
        self.cache[self.cache_key(route_id, poi_id)] = data

    def synthesize_story(self, *, text: str, language: str) -> bytes:
        self.logger.info("tts.synthesize_story", language=language)
        return self.provider.synthesize(
            text=text,
            language_code=language or settings.default_language,
            voice_name=settings.default_voice,
        )

    def synthesize(self, *, text: str, language_code: str, voice_name: str | None = None) -> bytes:
        self.logger.info("tts.synthesize", language_code=language_code)
        return self.provider.synthesize(
            text=text,
            language_code=language_code or settings.default_language,
            voice_name=voice_name or settings.default_voice,
        )
