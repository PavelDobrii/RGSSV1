# City Guide Backend

FastAPI service that builds city routes and optionally narrates them with synthesized speech. The backend combines Google
Directions, AI‑generated stories and text‑to‑speech to deliver a small “audio guide” for any walk.

## Features

- Generate walking or driving routes for a city using Google Directions
- Enrich points of interest with short AI‑written stories
- Convert stories to audio and cache the result for reuse
- Protect all endpoints with an API key

## Architecture Overview

- **Routes**: `/api/v1/routes` and `/api/v1/tts` defined in `app/routers`.
- **Services**: business logic in `app/services` handles route generation, text synthesis and caching.
- **Integrations**: adapters in `app/integrations` for third-party content and TTS providers.
- **Workflow**: generate a polyline via Google Directions → enrich with stories → optionally synthesize audio.

## Directory Structure

```
app/
  main.py            # application entry point
  routers/           # FastAPI routers
  services/          # route, TTS and map services
  integrations/      # external API adapters
  utils/             # helpers (cache, geometry)
tests/               # pytest test suite
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
make dev
```

## Logging

Logs use [structlog](https://www.structlog.org/) and can be customized via environment variables:

- `LOG_LEVEL` – set the log verbosity (e.g. `DEBUG`, `INFO`). Default is `INFO`.
- `LOG_FORMAT` – choose `JSON` for machine readable logs (default) or `PLAIN` for key-value output.

Example:

```bash
LOG_LEVEL=DEBUG LOG_FORMAT=plain make dev
```

## Test

```bash
make test
```

## Docker

```bash
make build
```

## API Examples

Generate route:

```bash
curl -X POST :8000/api/v1/routes/generate \
  -H "X-API-Key: devkey" -H "Content-Type: application/json" \
  -d '{"city":"Vilnius","start":{"lat":54.6872,"lng":25.2797},"duration_min":120,"transport_mode":"foot","interest_tags":["history"],"language":"en","need_audio":true}'
```

Synthesize text:

```bash
curl -X POST :8000/api/v1/tts/synthesize \
  -H "X-API-Key: devkey" -H "Content-Type: application/json" \
  -d '{"text":"Hello from CityGuide","language_code":"en-US"}' --output out.mp3
```

