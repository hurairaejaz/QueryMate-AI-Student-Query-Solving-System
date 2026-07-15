from pydantic import BaseModel, Field
from typing import Optional


class WhatsAppWebhookPayload(BaseModel):
    phone_number: str = Field(..., min_length=7)
    message_text: str = Field(..., min_length=1)
    name: Optional[str] = None