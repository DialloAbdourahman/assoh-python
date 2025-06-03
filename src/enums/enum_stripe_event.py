from enum import Enum

class EnumStripeEventType(Enum):
    CHECKOUT_SESSION_COMPLETED = 'checkout.session.completed'
    CHECKOUT_SESSION_EXPIRED = 'checkout.session.expired'
    PAYMENT_INTENT_FAILED = 'payment_intent.payment_failed'


