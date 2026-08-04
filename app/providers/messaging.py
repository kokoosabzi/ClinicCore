from abc import ABC, abstractmethod

from app.models.messaging import MessageProvider


class MessagingProvider(ABC):
    provider: MessageProvider

    @abstractmethod
    def send(self, recipient: str, body: str) -> None:
        raise NotImplementedError


class ConsoleMessageProvider(MessagingProvider):
    provider = MessageProvider.sms

    def send(self, recipient: str, body: str) -> None:
        print(f"[message:{self.provider}] {recipient}: {body}")


def get_provider(provider: MessageProvider) -> MessagingProvider:
    return ConsoleMessageProvider()
