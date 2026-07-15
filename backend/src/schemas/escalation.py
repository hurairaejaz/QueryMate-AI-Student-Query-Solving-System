from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AssignQueryRequest(BaseModel):
    assigned_to: int
    notes: Optional[str] = None


class EscalatedResponseCreate(BaseModel):
    response_text: str
    attachment_id: Optional[int] = None


class ResolveQueryRequest(BaseModel):
    notes: Optional[str] = None


class EscalatedQueryListItem(BaseModel):
    query_id: int
    query_text: str
    normalized_text: Optional[str] = None
    source: str
    status: str
    confidence_score: float = 0.0
    escalation_reason: Optional[str] = None
    assigned_to: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AssignQueryRequest(BaseModel):
    assigned_to: Optional[int] = None
    assigned_to_email: Optional[str] = None
    assigned_to_name: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True
        
class EscalatedQueryDetail(BaseModel):
    query_id: int
    query_text: str
    normalized_text: Optional[str] = None
    detected_language: Optional[str] = None
    intent_label: Optional[str] = None
    source: str
    status: str
    ai_response: Optional[str] = None
    confidence_score: float = 0.0
    escalation_reason: Optional[str] = None
    assigned_to: Optional[int] = None
    resolution_type: Optional[str] = None
    created_at: datetime
    last_response_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True