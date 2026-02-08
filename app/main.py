from fastapi import FastAPI, HTTPException
from pathlib import Path
import sqlite3
from datetime import datetime

app = FastAPI()

@app.on_event("startup")
def startup():
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

@app.post("/notes")
def create_note(title: str, body: str):
    if not title or not isinstance(title, str):
        raise HTTPException(status_code=422, detail="Title is required and must be a non-empty string")
    if not body or not isinstance(body, str):
        raise HTTPException(status_code=422, detail="Body is required and must be a non-empty string")
    
    # Get current UTC time in ISO-8601 format without microseconds
    created_at = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    
    # Insert note into database
    db_path = Path("data/app.db")
    conn = sqlite3.connect(db_path)
    
    cursor = conn.execute(
        "INSERT INTO notes (title, body, created_at) VALUES (?, ?, ?)",
        (title, body, created_at)
    )
    
    note_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Return the created note
    return {
        "id": note_id,
        "title": title,
        "body": body,
        "created_at": created_at
    }

@app.get("/health")
def health():
    return {"ok": True}