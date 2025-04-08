from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: Optional[str] = Field(default="Anonymous User")


class UserRead(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None)


class UserDeleteResponse(BaseModel):
    success: bool
    message: Optional[str] = Field(default=None)
