from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class MessageCreate(BaseModel):
    text: str = Field(min_length=1, max_length=5000)

    @field_validator("text")
    @classmethod
    def strip_text(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("text cannot be empty")
        return v


class MessageOut(BaseModel):
    id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("title cannot be empty")
        return v


class ChatOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: list[MessageOut] = []

    class Config:
        from_attributes = True
