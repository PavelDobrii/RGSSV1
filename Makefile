dev:
uvicorn app.main:app --reload

test:
pytest

build:
docker build -t city-guide .
