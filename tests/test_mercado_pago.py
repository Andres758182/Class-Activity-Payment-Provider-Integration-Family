from payment_integration.checkout_service import CheckoutService
from payment_integration.mercado_pago_payment_factory import MercadoPagoPaymentFactory
from payment_integration.payment_authorizer import PaymentAuthorizer
from payment_integration.refund_processor import RefundProcessor
from payment_integration.webhook_verifier import WebhookVerifier


def test_mercado_pago_family_is_selected_together():
    checkout = CheckoutService(MercadoPagoPaymentFactory())

    assert checkout.authorize_payment(125.50) == "mercado_pago:authorized:125.50"
    assert checkout.refund_payment(25.00) == "mercado_pago:refunded:25.00"
    assert checkout.verify_webhook("mercado-pago-valid") is True
    assert checkout.verify_webhook("stripe-valid") is False


def test_mercado_pago_factory_creates_a_complete_family():
    factory = MercadoPagoPaymentFactory()

    assert isinstance(factory.create_authorizer(), PaymentAuthorizer)
    assert isinstance(factory.create_refund_processor(), RefundProcessor)
    assert isinstance(factory.create_webhook_verifier(), WebhookVerifier)
