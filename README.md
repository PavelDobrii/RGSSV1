# City Guide Backend

FastAPI backend for generating city routes and synthesizing audio stories.

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
