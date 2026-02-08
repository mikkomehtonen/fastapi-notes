from fastapi import FastAPI, HTTPException, status
from pathlib import Path
import sqlite3
from datetime import datetime, timezone
from pydantic import BaseModel
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database directory if it doesn't exist
    Path("data").mkdir(exist_ok=True)
    
    # Create database file and notes table
    db_path = Path("data/app.db")
    conn = sqlite3.connect(db_path)
    
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

class NoteCreate(BaseModel):
    title: str
    body: str

class Note(BaseModel):
    id: int
    title: str
    body: str
    created_at: str

@app.post("/notes")
def create_note(note: NoteCreate):
    # Get current UTC time in ISO-8601 format without microseconds
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat() + "Z"
    
    # Insert note into database
    db_path = Path("data/app.db")
    conn = sqlite3.connect(db_path)
    
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
    db_path = Path("data/app.db")
    conn = sqlite3.connect(db_path)
    
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
    db_path = Path("data/app.db")
    conn = sqlite3.connect(db_path)
    
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

@app.get("/health")
def health():
    return {"ok": True}