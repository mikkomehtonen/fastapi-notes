from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(autouse=True)
def isolated_workdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    # Make sure "data/app.db" is created under a temp directory per test run.
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    yield


def test_health():
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json() == {"ok": True}

def test_post_and_list_roundtrip():
    with TestClient(app) as client:
        r = client.post("/notes", json={"title": "Hello", "body": "World"})
        assert r.status_code == 200
        created = r.json()

        assert isinstance(created["id"], int)
        assert created["id"] > 0
        assert created["title"] == "Hello"
        assert created["body"] == "World"
        assert "created_at" in created
        assert isinstance(created["created_at"], str)

        r2 = client.get("/notes")
        assert r2.status_code == 200
        notes = r2.json()
        assert isinstance(notes, list)
        assert any(n["id"] == created["id"] for n in notes)
