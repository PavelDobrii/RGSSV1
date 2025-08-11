import httpx
from typing import List, Tuple
import structlog
from ..schemas import TransportMode
from ..utils.geo import normalize_mode


class MapService:
    base_url = "https://maps.googleapis.com/maps/api/directions/json"

    def __init__(self, *, api_key: str):
        self.api_key = api_key
        self.logger = structlog.get_logger(__name__)

    async def build_polyline(self, points: List[Tuple[float, float]], mode: TransportMode) -> dict:
        if len(points) < 2:
            raise ValueError("at least two points required")
        gmode = normalize_mode(mode)
        origin = f"{points[0][0]},{points[0][1]}"
        destination = f"{points[-1][0]},{points[-1][1]}"
        waypoints = "|".join(f"{lat},{lng}" for lat, lng in points[1:-1])
        params = {
            "origin": origin,
            "destination": destination,
            "mode": gmode,
            "key": self.api_key,
        }
        if waypoints:
            params["waypoints"] = f"optimize:true|{waypoints}"
        self.logger.info("map.request", mode=gmode, waypoints=len(points))
        async with httpx.AsyncClient(timeout=6.0) as client:
            try:
                resp = await client.get(self.base_url, params=params)
                resp.raise_for_status()
            except httpx.HTTPError as exc:  # pragma: no cover - network errors
                self.logger.error("map.http_error", error=str(exc))
                raise RuntimeError(f"directions http error: {exc}") from exc
            data = resp.json()
        if data.get("status") != "OK":
            status = data.get("status", "unknown")
            error_message = data.get("error_message", "")
            self.logger.error("map.api_error", status=status, error_message=error_message)
            details = f"{status}: {error_message}" if error_message else status
            raise RuntimeError(f"directions error: {details}")
        route = data["routes"][0]
        legs = []
        total_distance = 0
        total_duration = 0
        for leg in route["legs"]:
            distance = leg["distance"]["value"]
            duration = leg["duration"]["value"]
            legs.append({"distance_m": distance, "duration_s": duration})
            total_distance += distance
            total_duration += duration
        self.logger.info(
            "map.response",
            total_distance_m=total_distance,
            total_duration_s=total_duration,
        )
        return {
            "polyline": route["overview_polyline"]["points"],
            "legs": legs,
            "total_distance_m": total_distance,
            "total_duration_s": total_duration,
        }
