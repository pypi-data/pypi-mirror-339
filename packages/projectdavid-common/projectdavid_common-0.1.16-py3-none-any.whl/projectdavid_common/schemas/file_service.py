from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FileUploadRequest(BaseModel):
    purpose: str = Field(..., description="Purpose for uploading the file")
    user_id: str = Field(..., description="ID of the uploading user")


class FileResponse(BaseModel):
    id: str
    object: str = "file"
    bytes: int
    created_at: int
    filename: str
    purpose: str
    status: str = "uploaded"
    expires_at: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
