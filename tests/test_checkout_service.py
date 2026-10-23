import inspect

import pytest

from payment_integration import checkout_service
from payment_integration.adyen_payment_factory import AdyenPaymentFactory
from payment_integration.checkout_service import CheckoutService
from payment_integration.payment_authorizer import PaymentAuthorizer
from payment_integration.payment_provider_factory import PaymentProviderFactory
from payment_integration.refund_processor import RefundProcessor
from payment_integration.stripe_payment_factory import StripePaymentFactory
from payment_integration.webhook_verifier import WebhookVerifier


def test_stripe_family_is_selected_together():
    checkout = CheckoutService(StripePaymentFactory())

    assert checkout.authorize_payment(125.50) == "stripe:authorized:125.50"
    assert checkout.refund_payment(25.00) == "stripe:refunded:25.00"
    assert checkout.verify_webhook("stripe-valid") is True
    assert checkout.verify_webhook("adyen-valid") is False


def test_adyen_family_is_selected_together():
    checkout = CheckoutService(AdyenPaymentFactory())

    assert checkout.authorize_payment(125.50) == "adyen:authorized:125.50"
    assert checkout.refund_payment(25.00) == "adyen:refunded:25.00"
    assert checkout.verify_webhook("adyen-valid") is True
    assert checkout.verify_webhook("stripe-valid") is False


def test_checkout_rejects_something_that_is_not_a_factory():
    with pytest.raises(TypeError):
        CheckoutService("mercado_pago")


def test_checkout_works_with_any_new_family_without_changes():
    class FakeAuthorizer(PaymentAuthorizer):
        def authorize(self, amount):
            return f"fake:authorized:{amount:.2f}"

    class FakeRefundProcessor(RefundProcessor):
        def refund(self, amount):
            return f"fake:refunded:{amount:.2f}"

    class FakeWebhookVerifier(WebhookVerifier):
        def verify(self, signature):
            return signature == "fake-valid"

    class FakePaymentFactory(PaymentProviderFactory):
        def create_authorizer(self):
            return FakeAuthorizer()

        def create_refund_processor(self):
            return FakeRefundProcessor()

        def create_webhook_verifier(self):
            return FakeWebhookVerifier()

    checkout = CheckoutService(FakePaymentFactory())

    assert checkout.authorize_payment(10.0) == "fake:authorized:10.00"
    assert checkout.refund_payment(5.0) == "fake:refunded:5.00"
    assert checkout.verify_webhook("fake-valid") is True


def test_checkout_does_not_import_provider_specific_classes():
    source = inspect.getsource(checkout_service).lower()

    for provider in ("stripe", "adyen", "mercado"):
        assert provider not in source
