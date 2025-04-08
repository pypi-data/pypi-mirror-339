from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class APIKeyRead(BaseModel):
    id: str = Field(..., description="The unique identifier for this API key")
    user_id: str = Field(..., description="User who owns the key")
    name: str = Field(..., description="Human-readable name of the key")
    created_at: int = Field(..., description="Unix timestamp of key creation")
    revoked: bool = Field(..., description="Whether the key has been revoked")
    revoked_at: Optional[int] = Field(None, description="Unix timestamp of revocation (if revoked)")

    model_config = ConfigDict(from_attributes=True)


class APIKeyCreate(BaseModel):
    user_id: str = Field(..., description="ID of the user creating the key")
    name: Optional[str] = Field(None, description="Optional human-readable name for the key")
    expires_at: Optional[datetime] = Field(
        None, description="Optional expiration date for the API key"
    )
