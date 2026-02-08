from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=20)
    body: str = Field(..., min_length=1)

class Note(BaseModel):
    id: int
    title: str
    body: str
    created_at: str

class NoteUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=20)
    body: str = Field(..., min_length=1)
