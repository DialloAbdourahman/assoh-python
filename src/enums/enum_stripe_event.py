from enum import Enum

class EnumStripeEventType(Enum):
    CHECKOUT_SESSION_COMPLETED = 'checkout.session.completed'
    PAYMENT_INTENT_FAILED = 'payment_intent.payment_failed'
    REFUND_CREATED = 'refund.created'
    REFUND_UPDATED = 'refund.updated'
    REFUND_FAILED = 'refund.failed'


