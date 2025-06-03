from stripe import stripe
from stripe.checkout import Session
from utils.config import stripe_secret_key
from models.order import Order

stripe.api_key = stripe_secret_key


class StripeService:
    @staticmethod
    def create_checkout_session(order:Order) -> Session:
        products = order.products

        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(product.price_at_order * 100),  # amount in cents
                    'product_data': {
                        'name': f'{product.product.name}',
                        'description': f'{product.product.description}',
                    },
                },
                'quantity': product.quantity,
            } for product in products]

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            metadata={
                'order_id': str(order.id),  # useful to track in webhook
            },
            success_url='https://yourapp.com/order/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://yourapp.com/order/cancel',
        )

        return checkout_session

        
# stripe listen --forward-to localhost:8000/assoh/api/v1/webhook 