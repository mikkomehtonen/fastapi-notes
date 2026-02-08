from fastapi import FastAPI
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

@app.get("/health")
def health():
    return {"ok": True}