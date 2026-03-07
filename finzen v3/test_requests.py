import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")
url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets") + "/v2/account"

headers = {
    "APCA-API-KEY-ID": api_key,
    "APCA-API-SECRET-KEY": secret_key
}

print(f"Testing URL: {url}")
try:
    print("Sending request...")
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"❌ Request Failed: {e}")
