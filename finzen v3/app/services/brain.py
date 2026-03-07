import json
import re
import sys
import os
from groq import Groq
from dotenv import load_dotenv
sys.path.append(os.getcwd())
from app.core.database import SessionLocal
from app.db.models import User, Budget, Transaction
from app.services.cfp_math import CFPLogicEngine
from app.services.calculators import FinancialCalculator
from app.services.rag_engine import FinZenMemory
from app.core.domain_rules import *
load_dotenv()
# --- CONFIGURATION --

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    print(f"✅ Loaded Groq Key: {GROQ_API_KEY[:5]}*****")
else:
    print("❌ ERROR: GROQ_API_KEY not found in environment!")
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"
# --- ROUTER PROMPT ---
ROUTER_PROMPT = """
You are the Intent Classifier for FinZen.
Map the user input to EXACTLY ONE category:

1. **TRADE_EXECUTION**: Explicit command to buy/sell a specific asset (e.g. "Buy Apple", "Invest $100").
   - NOTE: "Spending on snacks" is FINANCIAL_ADVISORY, NOT trade execution.
2. **STOCK_RESEARCH**: Asking for stock picks, comparisons, analysis ("What is best?", "Compare X and Y", "Show me high growth stocks").
3. **PROPERTY_RESEARCH**: Real estate queries ("Find flats in Mumbai", "Property in Bangalore", "Buy house").
4. **INSURANCE_RESEARCH**: Insurance queries ("Suggest health insurance", "Term life for 30 year old").
5. **TAX_PLANNING**: Tax calculations ("Calculate my tax", "Tax regime").
6. **SIP_CALCULATION**: SIP or Investment math ("SIP 5k for 10 years", "How much will I get?").
7. **FINANCIAL_ADVISORY**: "How do I recover?", "What did I do wrong?", "Budget help", "Emergency".
8. **GENERAL_CHAT**: Greetings, non-finance.

OUTPUT JSON: { "intent": "CATEGORY", "entities": ["list", "of", "names", "or", "locations"] }
"""

class FinZenBrain:
    def __init__(self, user_id=1):
        self.db = SessionLocal()
        self.user = self.db.query(User).filter(User.id == user_id).first()
        self.math_engine = CFPLogicEngine(self.user, self.user.debts)
        self.memory = FinZenMemory()

    # --- HELPERS ---
    def clean_json_text(self, text):
        """Fixes common JSON formatting errors from LLMs"""
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[-1]
            text = text.rsplit("\n", 1)[0]
        return text

    def extract_amount_heuristic(self, query):
        """Finds numbers in text (e.g., '5000' from 'Invest 5000')"""
        matches = re.findall(r'[\d,]+', query)
        if matches:
            try: return float(matches[0].replace(",", ""))
            except: return 0.0
        return 0.0

    def calculate_financials(self, tool, inputs):
        calc = FinancialCalculator()
        try:
            if tool == "sip_calculator": return calc.sip_future_value(inputs.get('amount',0), inputs.get('rate',12), inputs.get('years',10))
            if tool == "loan_emi": return calc.loan_emi(inputs.get('amount',0), inputs.get('rate',9), inputs.get('years',20))
            return 0
        except: return 0

    # --- CORE FUNCTIONS ---
    def detect_intent(self, query):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": ROUTER_PROMPT
                    },
                    {
                        "role": "user",
                        "content": f"QUERY: '{query}'\nOUTPUT JSON ONLY."
                    }
                ],
                model=MODEL_NAME,
                response_format={"type": "json_object"}
            )
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e: 
            print(f"Router Error: {e}")
            return {"intent": "GENERAL_CHAT", "entities": []}

    def consult(self, query, research_context=None, context_type="general"):
        # 1. Fetch Budget Context (Crucial for "What did I do wrong?")
        budgets = self.db.query(Budget).filter(Budget.user_id == self.user.id).all()
        budget_str = "\n".join([f"- {b.category}: Spent ₹{b.spent_so_far} / Limit ₹{b.limit_amount}" for b in budgets])

        # 2. Select System Prompt
        if context_type == "property":
            prompt = PROPERTY_SYSTEM_PROMPT
            user_context = f"DATA: Income ₹{self.user.monthly_income}, Cash ₹{self.user.emergency_fund_cash}. LISTINGS: {json.dumps(research_context)}"
        elif context_type == "insurance":
            prompt = INSURANCE_SYSTEM_PROMPT
            user_context = f"DATA: Age {self.user.age}, Income ₹{self.user.monthly_income * 12}. POLICIES: {json.dumps(research_context)}"
        elif context_type == "stock":
            prompt = STOCK_SYSTEM_PROMPT
            user_context = f"RISK: {self.user.risk_tolerance}. MARKET: {json.dumps(research_context)}"
        elif context_type == "tax":
            prompt = INDIAN_TAX_SYSTEM_PROMPT
            user_context = f"TAX DATA: Income ₹{self.user.monthly_income * 12}"
        else:
            # ADVISORY / GENERAL
            math_res = self.math_engine.run_analysis(0)
            past_mems = self.memory.recall(query)
            
            prompt = """
            You are FinZen, a Financial Mentor.
            RULES:
            1. Use the BUDGET STATUS below to answer "What did I do wrong?".
            2. Be helpful and detailed (Markdown).
            3. If user wants to TRADE (buy/sell assets), extract symbol/amount. Else symbol=null.
            
            OUTPUT SCHEMA (JSON): { "verdict": "INFO"|"APPROVE"|"WARNING", "response_text": "...", "extracted_symbol": null, "extracted_amount": 0.0, "tool_used": "none", "inputs_identified": {} }
            """
            
            user_context = f"""
            USER CONTEXT:
            - Income: ₹{self.user.monthly_income}
            - Risk Score: {math_res['risk_score']}
            - Emergency Fund: {math_res['emergency_coverage']} months
            
            🛑 BUDGET STATUS:
            {budget_str}
            
            MEMORIES: {past_mems}
            """

        # 3. Call Groq
        try:
            full_messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"{user_context}\nUSER QUERY: '{query}'"}
            ]
            
            chat_completion = client.chat.completions.create(
                messages=full_messages,
                model=MODEL_NAME,
                response_format={"type": "json_object"}
            )
            data = json.loads(chat_completion.choices[0].message.content)
            
            # Post-Process Math
            if context_type == "planning":
                tool = data.get('tool_used')
                if tool and tool != "none":
                    res = self.calculate_financials(tool, data.get('inputs_identified', {}))
                    data['response_text'] = f"Based on calculations, the result is ₹{res:,.2f}. {data.get('reasoning')}"

            # Memorize
            self.memory.memorize(f"Q: {query} | A: {data.get('response_text')[:50]}")
            return data
        
        except Exception as e:
            print(f"Brain Error: {e}")
            self.db.rollback() # Fix: Rollback transaction on error
            return {"verdict": "INFO", "response_text": f"I'm having trouble thinking clearly (Error: {str(e)}). Please try again.", "risk_score": 0}