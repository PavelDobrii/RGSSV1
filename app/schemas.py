from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class TransportMode(str, Enum):
    foot = "foot"
    bike = "bike"
    car = "car"
    public = "public"

class Point(BaseModel):
    lat: float
    lng: float

class RouteGenerateRequest(BaseModel):
    city: str
    start: Optional[Point] = None
    duration_min: int = Field(ge=30, le=240)
    transport_mode: TransportMode
    interest_tags: List[str] = Field(min_items=1, max_items=3)
    language: str | None = None
    need_audio: bool = False

class Stop(BaseModel):
    poi_id: str
    name: str
    lat: float
    lng: float
    story_text_md: str | None = None
    audio_url: str | None = None

class RouteResponse(BaseModel):
    route_id: str
    city: str
    polyline: str
    duration_min: int
    transport_mode: TransportMode
    stops: List[Stop]

class TTSSynthesizeRequest(BaseModel):
    text: str
    language_code: str
    voice_name: str | None = None

class ErrorResponse(BaseModel):
    detail: str
