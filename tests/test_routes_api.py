import pytest
from httpx import AsyncClient
from app.main import app
from app.schemas import TransportMode


@pytest.mark.asyncio
async def test_generate_route(monkeypatch):
    async def fake_build_polyline(self, points, mode):
        return {
            "polyline": "abc",
            "legs": [{"distance_m": 100, "duration_s": 60}, {"distance_m":100, "duration_s":60}],
            "total_distance_m": 200,
            "total_duration_s": 120,
        }

    def fake_propose_route(self, **kwargs):
        return [
            {"id": "p1", "name": "POI1", "lat": 1.0, "lng": 2.0, "poi_type": "", "draft_text": "draft1"},
            {"id": "p2", "name": "POI2", "lat": 1.1, "lng": 2.1, "poi_type": "", "draft_text": "draft2"},
        ]

    def fake_finalize_story(self, **kwargs):
        return "story"

    def fake_tts(self, **kwargs):
        return b"mp3"

    monkeypatch.setattr("app.services.map_service.MapService.build_polyline", fake_build_polyline)
    monkeypatch.setattr("app.integrations.content_ai.ContentAI.propose_route", fake_propose_route)
    monkeypatch.setattr("app.integrations.content_ai.ContentAI.finalize_story", fake_finalize_story)
    monkeypatch.setattr("app.integrations.tts_provider.TTSProvider.synthesize", fake_tts)

    payload = {
        "city": "Test",
        "start": {"lat": 1.0, "lng": 2.0},
        "duration_min": 120,
        "transport_mode": TransportMode.foot.value,
        "interest_tags": ["history"],
        "language": "en",
        "need_audio": True,
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/v1/routes/generate", json=payload, headers={"X-API-Key": "devkey"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["polyline"] == "abc"
    assert len(data["stops"]) == 2
    assert data["stops"][0]["audio_url"]
