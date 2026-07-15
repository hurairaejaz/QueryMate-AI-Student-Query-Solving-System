from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class AppQueryCreate(BaseModel):
    query_text: str = Field(..., min_length=2)
    department_key: str = "software_engineering"

class ChatDocumentOut(BaseModel):
     attachment_id: int
     file_name: Optional[str] = None
     file_url: Optional[str] = None
     open_url: Optional[str] = None
     mime_type: Optional[str] = None
     
     class Config:
        from_attributes = True
        
class QueryChatResponse(BaseModel):
    query_id: int
    status: str
    answer: Optional[str] = None
    confidence_score: float = 0.0
    resolution_type: Optional[str] = None
    documents: List[ChatDocumentOut] = []
    message: Optional[str] = None

    class Config:
        from_attributes = True

class QueryHistoryItem(BaseModel):
    query_id: int
    query_text: str
    status: str
    source: str
    created_at: datetime
    answer: Optional[str] = None
    confidence_score: float = 0.0
    resolution_type: Optional[str] = None

    class Config:
        from_attributes = True


class QueryDetailOut(BaseModel):
    query_id: int
    query_text: str
    normalized_text: Optional[str] = None
    detected_language: Optional[str] = None
    intent_label: Optional[str] = None
    status: str
    source: str
    ai_response: Optional[str] = None
    confidence_score: float = 0.0
    escalation_reason: Optional[str] = None
    resolution_type: Optional[str] = None
    created_at: datetime
    last_response_at: Optional[datetime] = None
    documents: List[ChatDocumentOut] = []

    class Config:
        from_attributes = True