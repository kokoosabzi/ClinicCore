from pydantic import BaseModel, ConfigDict, Field

from app.models.messaging import MessageProvider, MessageStatus


class MessageCreate(BaseModel):
    recipient: str = Field(min_length=3, max_length=120)
    provider: MessageProvider
    body: str = Field(min_length=1)


class MessageRead(MessageCreate):
    id: int
    status: MessageStatus
    error: str | None = None
    model_config = ConfigDict(from_attributes=True)
