from app.models.messaging import Message
from app.repositories.base import Repository


class MessageRepository(Repository[Message]):
    model = Message
