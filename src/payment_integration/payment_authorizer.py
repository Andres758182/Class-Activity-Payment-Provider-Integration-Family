from abc import ABC, abstractmethod


class PaymentAuthorizer(ABC):
    """Contrato: autorizar un pago."""

    @abstractmethod
    def authorize(self, amount: float) -> str:
        ...
