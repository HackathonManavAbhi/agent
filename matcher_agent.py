import requests
from uagents import Agent, Context
from utils.solana import call_solana_wallet_api

matcher = Agent(name="MatcherAgent")

SUPABASE_URL = "https://dqzfwqydxzjfrjnbsopi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRxemZ3cXlkeHpqZnJqbmJzb3BpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA0ODc2NDEsImV4cCI6MjA2NjA2MzY0MX0.7CHeu5ORvQZMsD7WD2IXSL3r5dMETycY1ob2CODI-us"
SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

@matcher.on_interval(period=30)  # Every 30 seconds
async def match_requests(ctx: Context):
    ctx.logger.info("Checking Supabase for matchable loans...")

    # Example: fetch loan_requests and loan_offers (simplified, unsecured version)
    loan_requests = requests.get(f"{SUPABASE_URL}/rest/v1/loan_requests", headers=SUPABASE_HEADERS).json()
    loan_offers = requests.get(f"{SUPABASE_URL}/rest/v1/loan_offers", headers=SUPABASE_HEADERS).json()

    # Find a simple match (same amount & duration)
    for req in loan_requests:
        for offer in loan_offers:
            if req['amount'] == offer['amount'] and req['duration_days'] == offer['duration_days']:
                ctx.logger.info(f"Found match: Request {req['id']} ⇄ Offer {offer['id']}")

                # Here: send messages to borrower and lender agents (if addresses known)
                # You'd typically use ctx.send or create an Agent Directory 


                # Inside your match logic:
                # response = call_solana_wallet_api(from_address=MATCHER_WALLET, to_address=offer['lender_wallet'], amount_sol=0.01, api_url=API_URL, api_key=API_KEY)
                # ctx.logger.info(f"Wallet transfer response: {response}")


if __name__ == "__main__":
    matcher.run()
# This code defines a MatcherAgent that periodically checks for matching loan requests and offers in a Supabase database.
# It uses the uagents framework to handle agent functionality and communication.
# The matcher looks for requests and offers with the same amount and duration, logging matches found.
# The matcher can be integrated into a multi-agent system where it interacts with BorrowerAgents and LenderAgents.