from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from app.core.database import SessionLocal
from app.db.models import User, Transaction
import os
from dotenv import load_dotenv
from pathlib import Path

# --- FORCE LOAD .ENV FROM ROOT ---
# This finds the root folder by going up 2 levels from app/services/
base_dir = Path(__file__).resolve().parents[2]
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

class InvestmentAgent:
    def __init__(self, user_id=1):
        self.db = SessionLocal()
        self.user = self.db.query(User).filter(User.id == user_id).first()
        self.client = None
        
        # 1. Try loading keys from Database
        api_key = self.user.alpaca_api_key
        secret_key = self.user.alpaca_secret_key

        # 2. If DB is empty, try loading from .env
        if not api_key:
            api_key = os.getenv("ALPACA_API_KEY")
            secret_key = os.getenv("ALPACA_SECRET_KEY")
            
            # Debugging: Print to console to prove it found them (Remove in prod)
            if api_key:
                print(f"   [DEBUG] Loaded Alpaca Key from .env: {api_key[:5]}*****")
            else:
                print("   [DEBUG] No Alpaca Key found in .env")

        # 3. Initialize Connection
        if api_key and secret_key:
            try:
                self.client = TradingClient(api_key, secret_key, paper=True)
                # Test connection
                self.client.get_account()
            except Exception as e:
                print(f"⚠️ Alpaca Connection Failed: {e}")
                self.client = None

    def link_account(self, key, secret):
        try:
            test = TradingClient(key, secret, paper=True)
            test.get_account()
            
            self.user.alpaca_api_key = key
            self.user.alpaca_secret_key = secret
            self.user.is_investor = True
            self.db.commit()
            
            self.client = test
            return "✅ Account Linked Successfully!"
        except Exception as e: return f"❌ Key Error: {e}"

    def execute_buy(self, symbol, amount_usd):
        if not self.client: 
            return "⚠️ Connection Error: No keys found. Check your .env file."
        
        print(f"📉 AGENT: Sending Order to NASDAQ for {symbol}...")
        try:
            req = MarketOrderRequest(
                symbol=symbol.upper(),
                notional=amount_usd,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )
            order = self.client.submit_order(req)
            
            tx = Transaction(
                user_id=self.user.id, amount=-amount_usd, 
                category="Investment", description=f"Bought ${amount_usd} of {symbol}"
            )
            self.db.add(tx)
            self.db.commit()
            
            return f"✅ SUCCESS: Bought ${amount_usd} of {symbol}. Order ID: {order.id}"
        except Exception as e: 
            self.db.rollback()
            return f"❌ Trade Rejected: {e}"