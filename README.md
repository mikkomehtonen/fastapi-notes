# Notes API (FastAPI + SQLite)

A small but complete CRUD application for notes, built with FastAPI, SQLite, and a minimal Jinja2-based UI.

The project was intentionally kept simple to serve as:
- a reference FastAPI backend
- a practical agent-assisted coding experiment
- a baseline for adding UIs on top of a stable API

## Features
- REST API for notes
  - Create, list, retrieve, update, delete
- SQLite persistence
- Input validation with Pydantic
- Proper HTTP status codes
- Automated tests with pytest
- ~99% test coverage
- Minimal HTML UI using Jinja2 + vanilla JavaScript

## Requirements
- Python 3.12+ (tested with 3.13)
- No external database
- No Node / npm / frontend build tools

## Setup

Create and activate a virtual environment:

```
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```
pip install -e .[test]
```

## Run the application
```
uvicorn app.main:app --reload --port 8080
```

## Open in browser:
- API health check: http://localhost:8080/health
- Notes UI: http://localhost:8080/

## Try the API manually
```
curl -s http://localhost:8080/health
```

## Create a note:
```
curl -s -X POST http://localhost:8080/notes -H 'Content-Type: application/json' -d '{"title":"Hei","body":"SQLite toimii"}'
```

## List notes:
```
curl -s http://localhost:8080/notes
```

## Tests

Run all tests:
```
python -m pytest -q
```

## Run tests with coverage:
```
coverage run -m pytest -q
coverage report -m
```

## Project structure
```
app/
  main.py # FastAPI app and endpoints
  models.py # Pydantic models
  init.py

templates/
  index.html # Minimal Jinja2 UI

test/
  test_api.py # API tests

data/
  app.db # SQLite database (created automatically)
```

## Notes
- The backend API is considered stable.
- The UI is intentionally minimal and framework-free.
- The project favors clarity and correctness over abstractions.
