from pydantic import BaseModel, Field, validator
from typing import List, Optional

class Point(BaseModel):
    lat: float
    lng: float

class RouteGenerateRequest(BaseModel):
    city: str
    start: Optional[Point] = None
    duration_min: int = Field(ge=30, le=240)
    transport_mode: str
    interest_tags: List[str] = Field(min_items=1, max_items=3)
    language: str | None = None
    need_audio: bool = False

    @validator("transport_mode")
    def check_mode(cls, v):
        if v not in {"foot", "bike", "car", "public"}:
            raise ValueError("unsupported mode")
        return v

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
    transport_mode: str
    stops: List[Stop]

class TTSSynthesizeRequest(BaseModel):
    text: str
    language_code: str
    voice_name: str | None = None

class ErrorResponse(BaseModel):
    detail: str
