import pytest

from payment_integration.adyen_payment_factory import AdyenPaymentFactory
from payment_integration.payment_authorizer import PaymentAuthorizer
from payment_integration.payment_provider_factory import PaymentProviderFactory
from payment_integration.refund_processor import RefundProcessor
from payment_integration.stripe_payment_factory import StripePaymentFactory
from payment_integration.webhook_verifier import WebhookVerifier


def test_factory_contract_cannot_be_instantiated():
    with pytest.raises(TypeError):
        PaymentProviderFactory()


def test_stripe_factory_creates_a_complete_family():
    factory = StripePaymentFactory()

    assert isinstance(factory.create_authorizer(), PaymentAuthorizer)
    assert isinstance(factory.create_refund_processor(), RefundProcessor)
    assert isinstance(factory.create_webhook_verifier(), WebhookVerifier)


def test_adyen_factory_creates_a_complete_family():
    factory = AdyenPaymentFactory()

    assert isinstance(factory.create_authorizer(), PaymentAuthorizer)
    assert isinstance(factory.create_refund_processor(), RefundProcessor)
    assert isinstance(factory.create_webhook_verifier(), WebhookVerifier)
