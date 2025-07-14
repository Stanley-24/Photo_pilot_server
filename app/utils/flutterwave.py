import httpx
import os

FLW_SECRET_KEY = os.getenv("FLW_SECRET_KEY")

async def verify_flutterwave_payment(transaction_id: str):
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {FLW_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        return None

    return response.json()
