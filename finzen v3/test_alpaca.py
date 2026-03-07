import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient

load_dotenv()

api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")

print(f"Testing Connectivity with:")
print(f"Key: {api_key}")
print(f"Secret: {secret_key[:5]}..." if secret_key else "Secret: None")

try:
    client = TradingClient(api_key, secret_key, paper=True)
    account = client.get_account()
    print("✅ Connection Successful!")
    print(f"Account Status: {account.status}")
    print(f"Buying Power: {account.buying_power}")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    import traceback
    traceback.print_exc()
