from abc import ABC, abstractmethod


class RefundProcessor(ABC):
    """Contrato: procesar un reembolso."""

    @abstractmethod
    def refund(self, amount: float) -> str:
        ...
