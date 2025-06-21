import requests

def call_solana_wallet_api(from_address: str, to_address: str, amount_sol: float, api_url: str, api_key: str = None) -> dict:
    """
    Calls an external API to trigger a Solana wallet transaction.

    Args:
        from_address (str): Sender's public wallet address.
        to_address (str): Recipient's public wallet address.
        amount_sol (float): Amount in SOL to transfer.
        api_url (str): Full endpoint URL for the transfer API.
        api_key (str, optional): Optional API key for authentication.

    Returns:
        dict: Response from the API call (JSON or error).
    """
    payload = {
        "from": from_address,
        "to": to_address,
        "amount": amount_sol
    }

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}