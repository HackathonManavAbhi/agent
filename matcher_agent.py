import requests
import os
from pyngrok import ngrok
from dotenv import load_dotenv
from uagents import Agent, Context, Protocol
from utils.stripe_util import (
    create_customer,
    attach_test_card,
    create_charge,
    transfer_to_connected_account
)

# load_dotenv()

public_url = ngrok.connect(8010)
print("🌐 Public endpoint:", public_url)

matcher = Agent(name="MatcherAgent", port=8010, endpoint=[public_url])
loan_protocol = Protocol(name="LoanProtocol")

# @matcher.on_interval(period=60)
# async def process_payment(ctx: Context):
#     customer = create_customer("borrower@example.com")
#     attach_test_card(customer["id"])
#     charge = create_charge(customer["id"], 5.00)  # Charge $5.00

#     ctx.logger.info(f"💳 Charge status: {charge['status']} | ID: {charge['id']}")


# @matcher.on_interval(period=30)  # Every 30 seconds
# async def match_requests(ctx: Context):
#     ctx.logger.info("Checking Supabase for matchable loans...")

#     # Example: fetch loan_requests and loan_offers (simplified, unsecured version)
#     loan_requests = requests.get(f"{os.getenv("SUPABASE_URL")}/rest/v1/loan_requests", headers=os.getenv("SUPABASE_HEADERS")).json()
#     loan_offers = requests.get(f"{os.getenv("SUPABASE_URL")}/rest/v1/loan_offers", headers=os.getenv("SUPABASE_HEADERS")).json()

#     # Find a simple match (same amount & duration)
#     for req in loan_requests:
#         for offer in loan_offers:
#             if req['amount'] == offer['amount'] and req['duration_days'] == offer['duration_days']:
#                 ctx.logger.info(f"Found match: Request {req['id']} ⇄ Offer {offer['id']}")

                # Here: send messages to borrower and lender agents (if addresses known)
                # You'd typically use ctx.send or create an Agent Directory 


                # Inside your match logic:
                # response = call_solana_wallet_api(from_address=MATCHER_WALLET, to_address=offer['lender_wallet'], amount_sol=0.01, api_url=API_URL, api_key=API_KEY)
                # ctx.logger.info(f"Wallet transfer response: {response}")


@loan_protocol.on_message
async def handle_loan_request(ctx: Context, sender: str, message: str):
    # Expecting message like: "borrower_email,amount,lender_account_id"
    try:
        borrower_email, amount_str, lender_account_id = message.split(",")
        amount = float(amount_str)
    except ValueError:
        ctx.logger.error("Invalid message format. Use: email,amount,account_id")
        return

    ctx.logger.info(f"💬 Received loan request: {amount} USD from {borrower_email} to {lender_account_id}")

    try:
        # Simulate borrower paying via card
        customer = create_customer(borrower_email)
        attach_test_card(customer["id"])
        charge = create_charge(customer["id"], amount)
        ctx.logger.info(f"💸 Charged borrower: {charge['status']}")

        # Simulate platform transferring funds to lender
        transfer = transfer_to_connected_account(lender_account_id, amount)
        ctx.logger.info(f"➡️ Transferred to lender: {transfer['status']} | ID: {transfer['id']}")

        await ctx.send(sender, f"✅ Loan processed. Stripe charge: {charge['id']}, Transfer: {transfer['id']}")

    except Exception as e:
        ctx.logger.error(f"❌ Error processing transaction: {e}")
        await ctx.send(sender, "❌ Loan processing failed. Please try again.")

matcher.include(loan_protocol)


if __name__ == "__main__":
    matcher.run()
# This code defines a MatcherAgent that periodically checks for matching loan requests and offers in a Supabase database.
# It uses the uagents framework to handle agent functionality and communication.
# The matcher looks for requests and offers with the same amount and duration, logging matches found.
# The matcher can be integrated into a multi-agent system where it interacts with BorrowerAgents and LenderAgents.