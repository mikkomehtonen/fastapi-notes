from fastapi import FastAPI, HTTPException, status, Request
from pathlib import Path
import sqlite3
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from .models import NoteCreate, Note, NoteUpdate
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

def get_db_connection():
    """Get a database connection to the notes database."""
    db_path = Path("data/app.db")
    return sqlite3.connect(db_path)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database directory if it doesn't exist
    Path("data").mkdir(exist_ok=True)

    # Create database file and notes table
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/notes")
def create_note(note: NoteCreate):
    # Get current UTC time in ISO-8601 format without microseconds
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat() + "Z"

    # Insert note into database
    conn = get_db_connection()

    cursor = conn.execute(
        "INSERT INTO notes (title, body, created_at) VALUES (?, ?, ?)",
        (note.title, note.body, created_at)
    )

    note_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Return the created note
    return {
        "id": note_id,
        "title": note.title,
        "body": note.body,
        "created_at": created_at
    }

@app.get("/notes", response_model=list[Note])
def get_notes():
    conn = get_db_connection()

    cursor = conn.execute("SELECT id, title, body, created_at FROM notes ORDER BY id DESC")
    notes = []
    for row in cursor.fetchall():
        notes.append({
            "id": row[0],
            "title": row[1],
            "body": row[2],
            "created_at": row[3]
        })

    conn.close()
    return notes

@app.get("/notes/{id}", response_model=Note)
def get_note(id: int):
    conn = get_db_connection()

    cursor = conn.execute("SELECT id, title, body, created_at FROM notes WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    return {
        "id": row[0],
        "title": row[1],
        "body": row[2],
        "created_at": row[3]
    }

@app.put("/notes/{id}", response_model=Note)
def update_note(id: int, note_update: NoteUpdate):
    conn = get_db_connection()

    cursor = conn.execute(
        "UPDATE notes SET title = ?, body = ? WHERE id = ?",
        (note_update.title, note_update.body, id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    # Retrieve the updated note
    conn = get_db_connection()
    cursor = conn.execute("SELECT id, title, body, created_at FROM notes WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    return {
        "id": row[0],
        "title": row[1],
        "body": row[2],
        "created_at": row[3]
    }

@app.delete("/notes/{id}")
def delete_note(id: int):
    conn = get_db_connection()

    cursor = conn.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    return {"message": "Note deleted successfully"}

@app.get("/health")
def health():
    return {"ok": True}
