from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class KBContentBase(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None
    department_key: str = "software_engineering"
    language: Optional[str] = "en"


class KBContentCreate(KBContentBase):
    pass

class KBContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    department_key: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[str] = None
    language: Optional[str] = None
    
    
class KBContentResponse(KBContentBase):
    kb_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
        
        
class AttachmentResponse(BaseModel):
    Kb_id: Optional[int] = None
    file_name: str
    file_url: str
    mime_type: Optional[str] = None

    class Config:
        from_attributes = True