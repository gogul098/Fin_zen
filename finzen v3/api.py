import sys
import os
import uvicorn
import json
import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union
from datetime import datetime

# Ensure Python sees your app modules
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.db.models import User, Budget, Asset, Goal, Commitment
from app.services.brain import FinZenBrain
from app.services.agent import InvestmentAgent
from app.services.researcher import MarketResearcher
from app.services.calculator import TaxCalculator, SIPCalculator, InsuranceAdvisor

# --- INIT APP ---
app = FastAPI(
    title="FinZen AI Backend",
    description="Agentic Financial Guardian API",
    version="V7.0"
)

# --- CORS (Allow Frontend Access) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for Hackathon demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INSTANTIATE SERVICES ---
# In production, use dependency injection (Depends)
# --- DATA MODELS ---
class ChatRequest(BaseModel):
    message: str
    user_id: Union[int, str] = 1 # Allow string IDs from frontend

class ContextRequest(BaseModel):
    user_id: int = 1
    context_text: str

class TradeRequest(BaseModel):
    user_id: int = 1
    symbol: str
    amount: float

# (Removed strict ChatResponse model usage on endpoint to allow dynamic UI Cards)

# --- HELPER: GRAPH DATA ---
def get_stock_history_data(symbol: str):
    """Fetches 1-month historical data for charts"""
    try:
        # Fix Ticker for India
        if not symbol.endswith(".NS") and not symbol.isupper():
            symbol = f"{symbol.upper()}.NS"
        
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")
        
        data_points = []
        for date, row in hist.iterrows():
            data_points.append({
                "date": date.strftime("%d %b"),
                "price": round(row['Close'], 1),
                "value": round(row['Close'], 1) # Added 'value' key for Recharts
            })
        return data_points
    except:
        return []

# ============================================================
#  ENDPOINTS
# ============================================================

@app.get("/")
def health_check():
    return {"status": "online", "system": "FinZen V7 Agent"}

# --- 1. DASHBOARD DATA ENDPOINT ---
@app.get("/dashboard/{user_id}")
def get_dashboard(user_id: int):
    """Aggregates all data for the Frontend Dashboard."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            # Fallback for demo if user DB is empty
            return {
                "user_name": "Siva",
                "net_worth": "₹12,50,000",
                "monthly_income": 85000,
                "daily_goal": "✅ Goal: Invest ₹500 in Nifty today.",
                "budget_pie": [
                    {"name": "Food", "value": 5000},
                    {"name": "Travel", "value": 3000},
                    {"name": "Rent", "value": 15000}
                ],
                "stock_graphs": []
            }

        # A. BUDGET PIE CHART
        budgets = db.query(Budget).filter(Budget.user_id == user_id).all()
        pie_data = []
        overspent_cats = []
        
        for b in budgets:
            if b.limit_amount > 0:
                pie_data.append({
                    "name": b.category,
                    "value": b.spent_so_far
                })
                if b.spent_so_far >= b.limit_amount:
                    overspent_cats.append(b.category)

        # B. STOCK GRAPHS (Top 2 Assets)
        assets = db.query(Asset).filter(Asset.user_id == user_id, Asset.asset_type.in_(["Stock", "Mutual Fund"])).limit(2).all()
        graphs = []
        
        for asset in assets:
            history = get_stock_history_data(asset.name)
            if history:
                graphs.append({
                    "symbol": asset.name,
                    "current_value": asset.current_value,
                    "data": history
                })

        # C. DAILY GOAL GENERATION
        if overspent_cats:
            daily_goal = f"⛔ STOP Spending on: {', '.join(overspent_cats[:2])}"
        else:
            daily_goal = "✅ Goal: Invest ₹500 in Nifty today."

        return {
            "user_name": user.username,
            "net_worth": f"₹{(user.monthly_income * 12) + user.emergency_fund_cash:,.0f}", # Simple proxy
            "monthly_income": user.monthly_income,
            "risk_score": 20, 
            "daily_goal": daily_goal,
            "budget_pie": pie_data,
            "stock_graphs": graphs
        }
    finally:
        db.close()

# --- 1.5 RECOMMENDATION ENDPOINTS (For Sidebar Menus) ---
@app.get("/recommendations/stock")
def get_stock_recs(user_id: int = 1):
    """Returns personalized stock picks based on risk profile."""
    # Mock logic: In real app, check user.risk_score
    return [
        {"symbol": "RELIANCE.NS", "name": "Reliance Industries", "price": 2450.0, "reason": "Stable Bluechip"},
        {"symbol": "TATAMOTORS.NS", "name": "Tata Motors", "price": 980.0, "reason": "High Growth Potential"},
        {"symbol": "HDFCBANK.NS", "name": "HDFC Bank", "price": 1650.0, "reason": "Banking Leader"},
        {"symbol": "INFY.NS", "name": "Infosys", "price": 1420.0, "reason": "Tech Defender"}
    ]

@app.get("/recommendations/property")
def get_property_recs(location: str = "Mumbai"):
    """Returns fresh property listings from web search."""
    # Use the Researcher
    researcher = MarketResearcher()
    properties = researcher.find_properties(location)
    return properties

# --- 2. CONTEXT UPDATE ENDPOINT ---
@app.post("/update-context")
async def update_personal_context(request: ContextRequest):
    """Saves user life updates (e.g., 'Getting married')."""
    brain.memory.memorize(f"USER LIFE UPDATE: {request.context_text}")
    return {"status": "success", "message": "Context memorized."}

# --- 2.5 PDF UPLOAD ENDPOINT ---
from fastapi import File, UploadFile
import shutil
from ingest_pdf import process_pdf

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), user_id: int = 1):
    """Uploads a PDF, extracts transactions, and deletes the file."""
    temp_file = f"temp_{file.filename}"
    
    try:
        # 1. Save locally
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Process
        count = process_pdf(temp_file)
        
        return {
            "status": "success",
            "message": f"Processed {count} transactions.",
            "transactions_count": count
        }
    except Exception as e:
        # Cleanup if error
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise HTTPException(status_code=500, detail=str(e))

# --- 2.7 DIRECT TRADE ENDPOINT ---
@app.post("/trade")
async def execute_trade(request: TradeRequest):
    """Direct UI trigger for executing trades."""
    agent = InvestmentAgent(user_id=request.user_id)
    trade_res = agent.execute_buy(request.symbol, request.amount)
    
    if "SUCCESS" in trade_res:
        return {"status": "success", "message": trade_res}
    else:
        raise HTTPException(status_code=400, detail=trade_res)

# --- 3. MAIN CHAT ENDPOINT ---
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    brain = FinZenBrain(user_id=request.user_id)
    agent = InvestmentAgent(user_id=request.user_id)
    researcher = MarketResearcher()
    user_input = request.message.strip()
    
    if not user_input:
        raise HTTPException(status_code=400, detail="Empty message")

    # A. HANDLE ONBOARDING (API KEYS)
    if user_input.startswith("PK") and len(user_input) > 10:
        res = agent.link_account(user_input, "dummy_secret_for_demo") 
        return {
            "role": "assistant",
            "type": "text",
            "content": f"🔑 {res}"
        }

    # B. DETECT INTENT (Semantic Router)
    intent_data = brain.detect_intent(user_input)
    intent = intent_data.get("intent", "GENERAL_CHAT")
    entities = intent_data.get("entities", [])

    context_type = "general"
    results = None
    action_status = "NONE"

    # C. ROUTE TO EXPERTS
    try:
        if intent == "STOCK_RESEARCH":
            context_type = "stock"
            results = researcher.compare_stocks(entities) if entities else researcher.find_best_stock()
            action_status = "RESEARCHED"

        elif intent == "PROPERTY_RESEARCH":
            context_type = "property"
            loc = "Mumbai"
            if "in" in user_input: loc = user_input.split("in")[-1].strip()
            results = researcher.find_properties(loc) 
            action_status = "RESEARCHED"

        elif intent == "INSURANCE_RESEARCH":
            context_type = "insurance"
            ins_type = "Health" if "medical" in user_input.lower() else "Term Life"
            # results = researcher.find_insurance(ins_type, brain.user.age, brain.user.monthly_income * 12)
            # Replaced with Calculator Logic
            avg_income = brain.user.monthly_income * 12
            suggestions = InsuranceAdvisor.suggest_coverage(brain.user.age, avg_income)
            results = suggestions
            action_status = "INSURANCE_SUGGESTED"

        elif intent == "TAX_PLANNING":
            context_type = "tax"
            # Extract income from input or use User DB
            income = brain.user.monthly_income * 12
            tax, regime = TaxCalculator.calculate_tax(income)
            
            results = {"tax": tax, "regime": regime, "income": income}
            response_text = f"Based on your annual income of ₹{income:,.0f}, your estimated tax is **₹{tax:,.0f}** under the {regime}."
            action_status = "CALCULATED"

        elif intent == "SIP_CALCULATION":
            context_type = "planning"
            # Default values if not extracted
            monthly = 5000
            years = 10
            rate = 12
            
            # Simple extraction heuristic (improve with NLP later)
            import re
            nums = re.findall(r'\d+', user_input.replace(",",""))
            if len(nums) >= 1: monthly = int(nums[0])
            if len(nums) >= 2: years = int(nums[1])
            
            fv = SIPCalculator.calculate_future_value(monthly, rate, years)
            invested = monthly * 12 * years
            gain = fv - invested
            
            results = {"monthly": monthly, "years": years, "rate": rate, "fv": fv, "invested": invested, "gain": gain}
            action_status = "SIP_CALCULATED"

        elif intent == "INSURANCE_RESEARCH":
            context_type = "insurance"
            avg_income = brain.user.monthly_income * 12
            suggestions = InsuranceAdvisor.suggest_coverage(brain.user.age, avg_income)
            results = suggestions
            action_status = "INSURANCE_SUGGESTED"

        elif intent == "FIN_CALC":
            context_type = "planning"
            action_status = "CALCULATED"

        elif intent == "TRADE_EXECUTION":
            context_type = "general"

        # D. CONSULT BRAIN
        decision = brain.consult(user_input, research_context=results, context_type=context_type)
        
        response_text = decision.get('response_text', '')
        verdict = decision.get('verdict', 'INFO')
        risk = decision.get('risk_score', 0)

        # E. EXECUTION LOGIC (Strict Gate)
        trade_details = None
        if intent == "TRADE_EXECUTION":
            sym = decision.get('extracted_symbol')
            amt = decision.get('extracted_amount')
            
            if sym and amt and amt > 0 and str(sym).lower() != "null":
                if verdict in ["APPROVE", "WARNING"]:
                    # EXECUTE TRADE
                    trade_res = agent.execute_buy(sym, amt)
                    response_text += f"\n\n🚀 **ACTION:** {trade_res}"
                    action_status = "TRADED"
                    trade_details = {"symbol": sym, "amount": amt}
                else:
                    response_text += f"\n\n🛑 **BLOCKED:** Trade rejected due to High Risk Score ({risk}/100)."
                    action_status = "BLOCKED"

        # =========================================================
        # F. FORMAT RESPONSE FOR REACT UI (STOCK CARDS / TICKETS)
        # =========================================================
        
        # Default: Text Response
        response_payload = {
            "role": "assistant",
            "type": "text",
            "content": response_text
        }

        # 1. UI Stock Card Logic
        if action_status == "RESEARCHED" and results:
            # Check if we have enough data for a card (Symbol + Price)
            # This depends on what 'results' structure your researcher returns
            # Assuming 'results' is a dict with 'symbol' and 'price'
            symbol_data = results if isinstance(results, dict) else {}
            
            # If researcher just returned text, try to extract symbol from entities
            target_symbol = symbol_data.get('symbol') or (entities[0] if entities else None)

            if target_symbol:
                history_data = get_stock_history_data(target_symbol)
                current_price = history_data[-1]['price'] if history_data else 0
                
                response_payload = {
                    "role": "assistant",
                    "type": "stock-card",
                    "data": {
                        "symbol": str(target_symbol).upper(),
                        "name": symbol_data.get('longName', 'Stock Asset'),
                        "price": current_price,
                        "change": 2.5, # Mock change if not available real-time
                        "history": history_data
                    }
                }
                # Prepend the text explanation
                response_payload["content"] = response_text

        # 2. UI Trade Ticket Logic
        elif action_status == "TRADED" and trade_details:
             response_payload = {
                "role": "assistant",
                "type": "trade-ticket",
                "data": {
                    "symbol": trade_details['symbol'],
                    "qty": trade_details['amount'],
                    "price": 100.0, # You can fetch real price here if needed
                    "status": "filled"
                }
             }
        
        # 3. UI Insurance Card
        elif action_status == "INSURANCE_SUGGESTED":
             response_payload = {
                "role": "assistant",
                "type": "insurance-card",
                "data": results, # List of policies
                "content": response_text
             }

        # 4. UI SIP Card
        elif action_status == "SIP_CALCULATED":
             response_payload = {
                "role": "assistant",
                "type": "sip-card",
                "data": results,
                "content": response_text
             }

        # 5. UI Tax Card
        elif action_status == "CALCULATED" and context_type == "tax":
             response_payload = {
                "role": "assistant",
                "type": "tax-card",
                "data": results,
                "content": response_text
             }

        return response_payload

    except Exception as e:
        print(f"Error: {e}")
        return {
            "role": "system",
            "type": "text",
            "content": f"I encountered a system error: {str(e)}"
        }

if __name__ == "__main__":
    print("🚀 FinZen API Starting on Port 8001...")
    uvicorn.run("api:app", host="0.0.0.0", port=8001, reload=True)