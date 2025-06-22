import requests
from uagents import Agent, Context
from utils.solana import call_solana_wallet_api

matcher = Agent(name="MatcherAgent", port=8002)

SUPABASE_URL = "https://dqzfwqydxzjfrjnbsopi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRxemZ3cXlkeHpqZnJqbmJzb3BpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA0ODc2NDEsImV4cCI6MjA2NjA2MzY0MX0.7CHeu5ORvQZMsD7WD2IXSL3r5dMETycY1ob2CODI-us"
SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

@matcher.on_interval(period=30)
async def match(ctx: Context):
    ctx.logger.info("MatcherAgent is running...")

    try:
        res1 = requests.get(f"{SUPABASE_URL}/rest/v1/loan_requests?select=*", headers=SUPABASE_HEADERS)
        res2 = requests.get(f"{SUPABASE_URL}/rest/v1/loan_offers?select=*", headers=SUPABASE_HEADERS)

        loan_requests = res1.json()
        loan_offers = res2.json()

        if isinstance(loan_requests, list) and isinstance(loan_offers, list):
            for req in loan_requests:
                for offer in loan_offers:
                    if req.get('amount') == offer.get('amount'):
                        ctx.logger.info(f"Matched Request {req['id']} with Offer {offer['id']}")
    except Exception as e:
        ctx.logger.error(f"Error in matcher: {str(e)}")

                # Here: send messages to borrower and lender agents (if addresses known)
                # You'd typically use ctx.send or create an Agent Directory 


                # Inside your match logic:
                # response = call_solana_wallet_api(from_address=MATCHER_WALLET, to_address=offer['lender_wallet'], amount_sol=0.01, api_url=API_URL, api_key=API_KEY)
                # ctx.logger.info(f"Wallet transfer response: {response}")


if __name__ == "__main__":
    matcher.run()