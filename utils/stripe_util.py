import stripe
import os
from dotenv import load_dotenv

load_dotenv()

MOCK_MODE = True

if not MOCK_MODE and stripe:
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_customer(email: str):
    if MOCK_MODE:
        return {"id": "cus_mock_123", "email": email}
    return stripe.Customer.create(email=email)

def attach_test_card(customer_id: str):
    if MOCK_MODE:
        return {"id": "card_mock_4242", "customer": customer_id}
    return stripe.Customer.create_source(customer_id, source="tok_visa")

def create_charge(customer_id: str, amount_usd: float):
    if MOCK_MODE:
        return {
            "id": "ch_mock_456",
            "status": "succeeded",
            "amount": int(amount_usd * 100),
            "customer": customer_id
        }
    return stripe.Charge.create(
        amount=int(amount_usd * 100),
        currency="usd",
        customer=customer_id,
        description="Mocked agent transaction"
    )


def create_connected_account():
    if MOCK_MODE:
        return {"id": "acct_mock_lender", "type": "express"}
    return stripe.Account.create(
        type="express",
        country="US",
        capabilities={"transfers": {"requested": True}}
    )


def transfer_to_connected_account(destination_account_id: str, amount_usd: float):
    if MOCK_MODE:
        return {
            "id": "tr_mock_789",
            "status": "succeeded",
            "destination": destination_account_id,
            "amount": int(amount_usd * 100)
        }
    return stripe.Transfer.create(
        amount=int(amount_usd * 100),
        currency="usd",
        destination=destination_account_id,
        description="Mocked loan transfer"
    )


if __name__ == "__main__":
    customer = create_customer("borrower@example.com")
    print("👤 Customer:", customer)

    card = attach_test_card(customer["id"])
    print("💳 Card:", card)

    charge = create_charge(customer["id"], 5.00)
    print("💸 Charge:", charge)

    lender = create_connected_account()
    print("🏦 Connected Account:", lender)

    transfer = transfer_to_connected_account(lender["id"], 3.00)
    print("➡️ Transfer:", transfer)