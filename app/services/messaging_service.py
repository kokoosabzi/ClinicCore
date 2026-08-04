from app.models.messaging import Message, MessageStatus
from app.providers.messaging import get_provider
from app.repositories.messaging_repository import MessageRepository
from app.schemas.messaging import MessageCreate


class MessagingService:
    def __init__(self, repository: MessageRepository) -> None:
        self.repository = repository

    def list_messages(self) -> list[Message]:
        return self.repository.list()

    def queue_message(self, data: MessageCreate) -> Message:
        return self.repository.create(Message(**data.model_dump()))

    def send_pending(self) -> int:
        sent = 0
        for message in self.repository.list():
            if message.status != MessageStatus.queued:
                continue
            provider = get_provider(message.provider)
            provider.send(message.recipient, message.body)
            message.status = MessageStatus.sent
            sent += 1
        self.repository.db.commit()
        return sent
