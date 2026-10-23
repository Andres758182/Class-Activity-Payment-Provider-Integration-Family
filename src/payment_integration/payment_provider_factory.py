from abc import ABC, abstractmethod

from .payment_authorizer import PaymentAuthorizer
from .refund_processor import RefundProcessor
from .webhook_verifier import WebhookVerifier


class PaymentProviderFactory(ABC):
    """Abstract Factory: crea la familia completa de componentes de un proveedor."""

    @abstractmethod
    def create_authorizer(self) -> PaymentAuthorizer:
        ...

    @abstractmethod
    def create_refund_processor(self) -> RefundProcessor:
        ...

    @abstractmethod
    def create_webhook_verifier(self) -> WebhookVerifier:
        ...
