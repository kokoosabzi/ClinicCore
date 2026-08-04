from enum import StrEnum

from sqlalchemy import Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import TimestampMixin


class MessageProvider(StrEnum):
    sms = "sms"
    email = "email"
    telegram = "telegram"
    whatsapp = "whatsapp"
    iranian_messenger = "iranian_messenger"


class MessageStatus(StrEnum):
    queued = "queued"
    sent = "sent"
    failed = "failed"


class Message(TimestampMixin, Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    recipient: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    provider: Mapped[MessageProvider] = mapped_column(Enum(MessageProvider), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[MessageStatus] = mapped_column(Enum(MessageStatus), default=MessageStatus.queued, nullable=False)
    error: Mapped[str | None] = mapped_column(Text)
