# Notes API (FastAPI + SQLite)

A small but complete CRUD application for notes, built with FastAPI, SQLite, and a minimal Jinja2-based UI.

This project was also an experiment in using a **small, locally hosted language model (~30B parameters)** as a coding agent,
instead of relying on large hosted systems such as Claude Code or OpenAI Codex.

The implementation was developed using:
- **qwen3-coder** with a **32k context window**
- **Ollama** for local model execution
- **OpenCode** as the agent orchestration environment

The goal was to explore how far a constrained, fully local setup can go when:
- the scope is clearly defined
- the human stays in the loop
- correctness and clarity are prioritized over speed

The result demonstrates that even relatively small models can be effective assistants for real, end-to-end software projects when used deliberately.

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

## Demo UI

This project includes a small, intentionally minimal web UI built with Jinja2 and Tailwind CSS.

The UI is not meant to be a full frontend framework, but a **demo-quality interface** that makes the API easy to explore and present to non-technical users.

### Features
- Create, edit and delete notes
- Inline editing directly on note cards
- Friendly empty-state and clear call-to-action
- Subtle hover and fade-in animations for perceived quality
- Clean, modern visual style suitable for demos

The UI is deliberately simple:
- no frontend build step
- no JavaScript framework
- no client-side state management

It exists to demonstrate how a small, well-tested FastAPI backend can be paired with a presentable UI with very little overhead.

### Design philosophy

This project favors:
- clarity over abstraction
- correctness over cleverness
- minimalism as a conscious design choice

The goal was not to build “the perfect notes app”, but a **complete, understandable, and demo-ready system**.

## Notes
- The backend API is considered stable.
- The UI is intentionally minimal and framework-free.
- The project favors clarity and correctness over abstractions.

This project was built using agent-assisted development, with the human in the loop guiding design, scope and correctness.
