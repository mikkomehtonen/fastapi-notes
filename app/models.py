from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    body: str

class Note(BaseModel):
    id: int
    title: str
    body: str
    created_at: str

class NoteUpdate(BaseModel):
    title: str
    body: str
