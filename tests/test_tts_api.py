import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_tts_synthesize(monkeypatch):
    def fake_tts(self, **kwargs):
        return b"mp3"

    monkeypatch.setattr("app.integrations.tts_provider.TTSProvider.synthesize", fake_tts)

    payload = {"text": "Hello", "language_code": "en-US"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/v1/tts/synthesize", json=payload, headers={"X-API-Key": "devkey"})
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "audio/mpeg"
    assert await resp.aread() == b"mp3"
