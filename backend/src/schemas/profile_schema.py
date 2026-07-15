# CHANGE: Schema for profile update request

from pydantic import BaseModel, Field


class ProfileUpdateRequest(BaseModel):
    full_name: str = Field(..., min_length=2)
    phone: str = Field(..., pattern=r"^03\d{9}$")