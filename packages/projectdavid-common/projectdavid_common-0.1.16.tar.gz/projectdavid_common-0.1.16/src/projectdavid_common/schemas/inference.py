from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from projectdavid_common.schemas.enums import ProviderEnum


class ProcessOutput(BaseModel):
    store_name: str
    status: str
    chunks_processed: int

    model_config = ConfigDict(from_attributes=True)


class StreamRequest(BaseModel):
    provider: ProviderEnum = Field(..., description="The inference provider")
    model: str = Field(..., description="The model to use for inference")
    api_key: Optional[str] = Field(None, description="Optional API key for third-party providers")
    thread_id: str = Field(..., description="Thread identifier")
    message_id: str = Field(..., description="Message identifier")
    run_id: str = Field(..., description="Run identifier")
    assistant_id: str = Field(..., description="Assistant identifier")

    model_config = ConfigDict(from_attributes=True)
