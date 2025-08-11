import asyncio
import uuid
from typing import List, Tuple

import structlog

from ..integrations.content_ai import ContentAI
from ..schemas import TransportMode
from ..services.map_service import MapService
from ..services.tts_service import TTSService


class RouteService:
    def __init__(self, content_ai: ContentAI, map_service: MapService, tts_service: TTSService):
        self.content_ai = content_ai
        self.map_service = map_service
        self.tts_service = tts_service
        self.logger = structlog.get_logger(__name__)

    async def generate_route(
        self,
        *,
        city: str,
        start: Tuple[float, float] | None,
        duration_min: int,
        transport_mode: TransportMode,
        interest_tags: List[str],
        language: str,
        need_audio: bool,
    ) -> dict:
        self.logger.info("route.generate", city=city, transport_mode=transport_mode)
        pois = self.content_ai.propose_route(
            city=city,
            start=start,
            duration_min=duration_min,
            transport_mode=transport_mode,
            interest_tags=interest_tags,
        )
        if not pois:
            route = {
                "route_id": str(uuid.uuid4()),
                "city": city,
                "polyline": "",
                "duration_min": 0,
                "transport_mode": transport_mode,
                "stops": [],
            }
            self.logger.info("route.empty", route_id=route["route_id"], city=city)
            return route
        points = [(p["lat"], p["lng"]) for p in pois]
        map_data = await self.map_service.build_polyline(points, transport_mode)
        route_id = str(uuid.uuid4())
        self.logger.info("route.created", route_id=route_id, stops=len(pois))
        stops = []
        duration_acc = 0
        for idx, poi in enumerate(pois):
            leg_duration = map_data["legs"][idx]["duration_s"] if idx < len(map_data["legs"]) else 0
            duration_acc += leg_duration
            if duration_acc > duration_min * 60:
                break
            story_text = poi.get("draft_text", "")
            if need_audio:
                story_text = await asyncio.to_thread(
                    self.content_ai.finalize_story,
                    poi_id=poi["id"],
                    draft_text=story_text,
                    language=language,
                )
                audio = await asyncio.to_thread(
                    self.tts_service.synthesize_story,
                    text=story_text,
                    language=language,
                )
                self.tts_service.set_cached(route_id, poi["id"], audio)
                audio_url = f"/api/v1/tts/by-id?rid={route_id}&poi={poi['id']}"
            else:
                audio_url = None
            stops.append({
                "poi_id": poi["id"],
                "name": poi["name"],
                "lat": poi["lat"],
                "lng": poi["lng"],
                "story_text_md": story_text if need_audio else None,
                "audio_url": audio_url,
            })
        result = {
            "route_id": route_id,
            "city": city,
            "polyline": map_data["polyline"],
            "duration_min": int(map_data["total_duration_s"] / 60),
            "transport_mode": transport_mode,
            "stops": stops,
        }
        self.logger.info("route.complete", route_id=route_id, stops=len(stops))
        return result
