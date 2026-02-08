import sys
import os

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


def test_get_note():
    with TestClient(app) as client:
        # Create a note first
        r = client.post("/notes", json={"title": "Test Note", "body": "Test Body"})
        assert r.status_code == 200
        created = r.json()

        r2 = client.get(f"/notes/{created['id']}")
        assert r2.status_code == 200
        note = r2.json()
        assert note["id"] == created["id"]
        assert note["title"] == "Test Note"
        assert note["body"] == "Test Body"
        assert note["created_at"] == created["created_at"]


def test_get_note_not_found():
    with TestClient(app) as client:
        r = client.get("/notes/999")
        assert r.status_code == 404
        assert r.json() == {"detail": "Note not found"}


def test_update_note():
    with TestClient(app) as client:
        # Create a note first
        r = client.post("/notes", json={"title": "Test Note", "body": "Test Body"})
        assert r.status_code == 200
        created = r.json()

        # Update the note
        r2 = client.put(f"/notes/{created['id']}", json={"title": "Updated Title", "body": "Updated Body"})
        assert r2.status_code == 200
        updated = r2.json()
        assert updated["id"] == created["id"]
        assert updated["title"] == "Updated Title"
        assert updated["body"] == "Updated Body"
        assert updated["created_at"] == created["created_at"]


def test_update_note_not_found():
    with TestClient(app) as client:
        r = client.put("/notes/999", json={"title": "Updated Title", "body": "Updated Body"})
        assert r.status_code == 404
        assert r.json() == {"detail": "Note not found"}


def test_delete_note():
    with TestClient(app) as client:
        # Create a note first
        r = client.post("/notes", json={"title": "Test Note", "body": "Test Body"})
        assert r.status_code == 200
        created = r.json()

        # Delete the note
        r2 = client.delete(f"/notes/{created['id']}")
        assert r2.status_code == 200
        assert r2.json() == {"message": "Note deleted successfully"}

        # Verify the note is gone
        r3 = client.get(f"/notes/{created['id']}")
        assert r3.status_code == 404
        assert r3.json() == {"detail": "Note not found"}


def test_delete_note_not_found():
    with TestClient(app) as client:
        r = client.delete("/notes/999")
        assert r.status_code == 404
        assert r.json() == {"detail": "Note not found"}


def test_create_note_with_empty_title():
    with TestClient(app) as client:
        r = client.post("/notes", json={"title": "", "body": "Test Body"})
        assert r.status_code == 422


def test_create_note_with_empty_body():
    with TestClient(app) as client:
        r = client.post("/notes", json={"title": "Test Title", "body": ""})
        assert r.status_code == 422


def test_create_note_with_title_too_long():
    with TestClient(app) as client:
        r = client.post("/notes", json={"title": "This title is longer than twenty characters", "body": "Test Body"})
        assert r.status_code == 422


def test_update_note_with_empty_title():
    with TestClient(app) as client:
        # Create a note first
        r = client.post("/notes", json={"title": "Test Note", "body": "Test Body"})
        assert r.status_code == 200
        created_note = r.json()

        # Try to update with empty title
        r2 = client.put(f"/notes/{created_note['id']}", json={"title": "", "body": "Updated Body"})
        assert r2.status_code == 422


def test_update_note_with_empty_body():
    with TestClient(app) as client:
        # Create a note first
        r = client.post("/notes", json={"title": "Test Note", "body": "Test Body"})
        assert r.status_code == 200
        created_note = r.json()

        # Try to update with empty body
        r2 = client.put(f"/notes/{created_note['id']}", json={"title": "Updated Title", "body": ""})
        assert r2.status_code == 422


def test_update_note_with_title_too_long():
    with TestClient(app) as client:
        # Create a note first
        r = client.post("/notes", json={"title": "Test Note", "body": "Test Body"})
        assert r.status_code == 200
        created_note = r.json()

        # Try to update with title too long
        r2 = client.put(f"/notes/{created_note['id']}", json={"title": "This title is longer than twenty characters", "body": "Updated Body"})
        assert r2.status_code == 422
