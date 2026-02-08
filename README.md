# Notes API (FastAPI + SQLite)

## Run
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]

uvicorn app.main:app --reload --port 8080

## Try
curl -s http://localhost:8080/health
curl -s -X POST http://localhost:8080/notes -H 'Content-Type: application/json' -d '{"title":"Hei","body":"SQLite toimii"}'
curl -s http://localhost:8080/notes

## Tests
pytest -q
