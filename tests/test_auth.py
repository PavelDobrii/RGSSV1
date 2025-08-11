import sys
from pathlib import Path

import asyncio

import pytest
from httpx import AsyncClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app


def test_api_key_required():
    async def run_test():
        async with AsyncClient(app=app, base_url="http://test") as ac:
            resp = await ac.post(
                "/api/v1/tts/synthesize",
                json={"text": "Hello", "language_code": "en-US"},
                headers={"X-API-Key": "wrong"},
            )
        assert resp.status_code == 401

    asyncio.run(run_test())
