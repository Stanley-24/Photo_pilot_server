import requests
import os

PEXELS_API_KEY = os.getenv("Pexels")  # Put your Pexels API key in .env

def get_pexels_backgrounds(query="nature", per_page=5):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    # Return list of URLs of medium size photos
    return [photo["src"]["medium"] for photo in data.get("photos", [])]
