from fastapi import APIRouter, HTTPException, Header, Request
from enums.enum_stripe_event import EnumStripeEventType
import stripe
from utils.config import stripe_webhook_key
from services.webhook import WebhookService

router = APIRouter(tags=['Webhook'])

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature")
):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=stripe_webhook_key
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    try:
        event_type = event['type']
        session = event['data']['object']

        if event_type == EnumStripeEventType.CHECKOUT_SESSION_COMPLETED.value:
            order_id = session.get('metadata', {}).get('order_id')
            payment_intent_id = session.get('payment_intent')
            WebhookService.checkout_success(order_id, payment_intent_id)

        elif event_type == EnumStripeEventType.PAYMENT_INTENT_FAILED.value:
            order_id = session.get('metadata', {}).get('order_id')
            payment_intent_id = session.get('id')
            WebhookService.payment_intent_failed(order_id=order_id, payment_intent_id=payment_intent_id)

        elif event_type == EnumStripeEventType.REFUND_CREATED.value:
            refund_id = session.get('id')
            WebhookService.handle_refund_created(refund_id=refund_id)

        elif event_type == EnumStripeEventType.REFUND_UPDATED.value:
            refund_id = session.get('id')
            status = session.get('status')
            if status == 'succeeded':
                WebhookService.handle_refund_succeeded(refund_id=refund_id)

        elif event_type == EnumStripeEventType.REFUND_FAILED.value:
            refund_id = session.get('id')
            WebhookService.handle_refund_failed(refund_id=refund_id)

    except Exception as e:
        print(f"Error handling Stripe event: {e}")
        raise HTTPException(status_code=500, detail="Internal webhook processing error")

    return {"status": "success"}
