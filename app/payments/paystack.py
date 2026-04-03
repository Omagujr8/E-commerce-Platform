import requests
from app.core.config import settings


PAYSTACK_BASE_URL = "https://api.paystack.co"


def initialize_payment(email: str, amount: float):
    url = f"{PAYSTACK_BASE_URL}/transaction/initialize"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "email": email,
        "amount": int(amount * 100),  # convert to kobo
    }

    response = requests.post(url, json=data, headers=headers)

    return response.json()


def verify_payment(reference: str):
    url = f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(url, headers=headers)

    return response.json()