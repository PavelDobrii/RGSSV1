# City Guide Backend

FastAPI backend for generating city routes and synthesizing audio stories.

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

## Замечания по коду и рекомендации

README содержит инструкции по установке и примеры, но нет описания структуры проекта и архитектуры, что затрудняет быстрое погружение в кодовую базу​:codex-file-citation[codex-file-citation]{line_range_start=1 line_range_end=60 path=README.md git_url="https://github.com/PavelDobrii/RGSSV1/blob/main/README.md#L1-L60"}​

:::task-stub{title="Расширить README проектным обзором"}
1. Открыть `README.md`.
2. Добавить разделы “Обзор архитектуры” и “Структура каталогов”, описывающие `app/`, `services/`, `routers/`, `integrations/` и `tests/`.
3. Включить краткую схему работы (генерация маршрута → обогащение контентом → синтез аудио).
:::

Метод `MapService.build_polyline` при ошибке Directions API выдает общее сообщение `"directions error"`, без деталей о причине, что усложняет диагностику​:codex-file-citation[codex-file-citation]{line_range_start=31 line_range_end=36 path=app/services/map_service.py git_url="https://github.com/PavelDobrii/RGSSV1/blob/main/app/services/map_service.py#L31-L36"}​

:::task-stub{title="Уточнить ошибки Google Directions API"}
1. В `app/services/map_service.py` обернуть запрос в `try/except httpx.HTTPError`.
2. В случае `data["status"] != "OK"` логировать код ошибки и сообщение из `data`.
3. Возвращать `HTTPException` или `RuntimeError` с подробностями ответа API.
:::

`RouteService.generate_route` выполняет синхронные вызовы `ContentAI.finalize_story` и `TTSService.synthesize_story` внутри асинхронного контекста, что может блокировать event loop​:codex-file-citation[codex-file-citation]{line_range_start=58 line_range_end=63 path=app/services/route_service.py git_url="https://github.com/PavelDobrii/RGSSV1/blob/main/app/services/route_service.py#L58-L63"}​

:::task-stub{title="Избежать блокировок в RouteService"}
1. В `app/services/route_service.py` использовать `await asyncio.to_thread(...)` для вызовов `finalize_story` и `synthesize_story`, либо сделать их асинхронными.
2. Добавить соответствующие тесты производительности для подтверждения отсутствия блокировок.
:::

Проект тестирует базовые успешные сценарии, но не покрывает ошибки интеграций и кеширования, например, поведение `MapService` при недоступности API или промахи TTS-кеша.

:::task-stub{title="Расширить тестовое покрытие нештатных ситуаций"}
1. В каталоге `tests/` добавить тесты для:
   - сбоя Google Maps (e.g. `RuntimeError` из `build_polyline`);
   - запроса аудио по отсутствующему ключу (ожидаемый `404`).
2. Использовать `pytest` и `monkeypatch` для имитации HTTP‑ошибок и пустого кеша.
:::

