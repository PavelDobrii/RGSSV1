import sys
from pathlib import Path

import asyncio

import pytest
from httpx import AsyncClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.deps import get_tts_service
from app.main import app


def test_tts_synthesize(monkeypatch):
    get_tts_service.cache_clear()

    def fake_tts(self, **kwargs):
        return b"mp3"

    monkeypatch.setattr("app.integrations.tts_provider.TTSProvider.synthesize", fake_tts)

    payload = {"text": "Hello", "language_code": "en-US"}
    async def run_test():
        async with AsyncClient(app=app, base_url="http://test") as ac:
            resp = await ac.post("/api/v1/tts/synthesize", json=payload, headers={"X-API-Key": "devkey"})
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "audio/mpeg"
        assert await resp.aread() == b"mp3"

    asyncio.run(run_test())
