import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount: float):
    intent = stripe.PaymentIntent.create(
        amount=int(amount *100),  # convert to kobo/cents
        currency = "usd",
        payment_method_types = ["card"],
    )
    return intent
