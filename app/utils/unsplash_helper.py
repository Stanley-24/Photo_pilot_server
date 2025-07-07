import requests
import os
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("Unsplash")

def get_unsplash_backgrounds(query="nature", per_page=5):
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {"query": query, "per_page": per_page}
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    data = res.json()
    return [item["urls"]["regular"] for item in data.get("results", [])]
