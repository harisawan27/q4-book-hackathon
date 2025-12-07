from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class VectorChunk(BaseModel):
    content: str
    source_file: str
    url_slug: str
    header_path: str
    chunk_index: int

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    selected_text: Optional[str] = None
    page_context: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    citations: List[str]

class Interaction(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: str
    selected_context: Optional[str] = None
    created_at: datetime
