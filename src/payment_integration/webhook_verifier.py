from abc import ABC, abstractmethod


class WebhookVerifier(ABC):
    """Contrato: verificar la firma de un webhook."""

    @abstractmethod
    def verify(self, signature: str) -> bool:
        ...
