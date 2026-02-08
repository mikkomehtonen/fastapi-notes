from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    """Data model for creating a new note.

    Attributes:
        title: The title of the note (1-20 characters, required)
        body: The content of the note (required)
    """
    title: str = Field(..., min_length=1, max_length=20)
    body: str = Field(..., min_length=1)

class Note(BaseModel):
    """Data model representing a note with its ID and creation timestamp.

    Attributes:
        id: Unique identifier for the note
        title: The title of the note (1-20 characters, required)
        body: The content of the note (required)
        created_at: ISO format timestamp when the note was created
    """
    id: int
    title: str
    body: str
    created_at: str

class NoteUpdate(BaseModel):
    """Data model for updating an existing note.

    Attributes:
        title: The title of the note (1-20 characters, optional)
        body: The content of the note (optional)
    """
    title: str = Field(..., min_length=1, max_length=20)
    body: str = Field(..., min_length=1)
