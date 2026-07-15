from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ResponseCreate(BaseModel):
    query_id: int
    response_text: str
    response_type: str = "ai"
    responder_id: Optional[int] = None
    confidence_score: float = 0.0
    tone_used: Optional[str] = None
    source_evidence: Optional[str] = None
    attachment_id: Optional[int] = None


class ResponseOut(BaseModel):
    response_id: int
    query_id: int
    response_text: str
    response_type: str
    responder_id: Optional[int] = None
    confidence_score: float = 0.0
    tone_used: Optional[str] = None
    source_evidence: Optional[str] = None
    attachment_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True