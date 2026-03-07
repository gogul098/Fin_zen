import yfinance as yf
from duckduckgo_search import DDGS
import json
import requests
from groq import Groq
import os
import time

# --- CONFIGURATION ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
# Using same large model for researcher as it needs good reasoning for parsing
MODEL_NAME = "llama-3.3-70b-versatile"

class MarketResearcher:
    def __init__(self):
        # Default fallback list
        self.default_watchlist = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "TATAMOTORS.NS"]

        # Verification Portals (For Forensic Checks)
        self.rera_portals = {
            "Maharashtra": "https://maharera.maharashtra.gov.in/",
            "Karnataka": "https://rera.karnataka.gov.in/",
            "Uttar Pradesh": "https://www.up-rera.in/",
            "Tamil Nadu": "https://www.rera.tn.gov.in/"
        }

    # ============================================================
    #  CORE 1: WEB SEARCH ENGINE (The Eyes)
    # ============================================================
    def search_web(self, query, max_results=4):
        """Searches DuckDuckGo and returns raw text results."""
        print(f"   🔎 Searching Web: '{query}'...")
        try:
            with DDGS() as ddgs:
                # 'text' is the stable method for text search
                results = list(ddgs.text(query, max_results=max_results))
                return results
        except Exception as e:
            print(f"   ⚠️ Search Error: {e}")
            return []

    # ============================================================
    #  CORE 2: INTELLIGENT PARSER (The Filter)
    # ============================================================
    def clean_and_extract(self, raw_results, extraction_type):
        """
        Uses Groq (Llama 3) to read raw search results and extract STRUCTURED DATA.
        """
        if not raw_results: return []
        
        prompt_map = {
            "property": """
                Analyze these search results for Real Estate.
                TASK: Extract a list of distinct properties found.
                RULES: 
                1. Convert prices like '85 Lacs', '1.2 Cr' into pure numbers (e.g. 8500000).
                2. Extract Location and Name.
                OUTPUT JSON: [ {"name": "Property Name", "location": "Loc", "price_inr": <number>, "type": "2BHK/3BHK"} ]
            """,
            "insurance": """
                Analyze these search results for Insurance Policies.
                TASK: Extract policy details.
                RULES: Estimate premiums if mentioned.
                OUTPUT JSON: [ {"policy_name": "Name", "insurer": "Company", "sum_assured": "Text (e.g. 1 Cr)", "annual_premium_est": <number>} ]
            """
        }

        prompt = f"""
        CONTEXT: I searched the web and got these raw results:
        {json.dumps(raw_results)}

        TASK: {prompt_map.get(extraction_type, "Summarize")}
        
        OUTPUT STRICT JSON ONLY. NO MARKDOWN.
        """
        
        try:
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a Data Extractor. Output strictly valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                model=MODEL_NAME,
                response_format={"type": "json_object"}
            )
            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            print(f"   ⚠️ Parsing Error: {e}")
            return raw_results # Fallback to raw text if AI fails

    # ============================================================
    #  3. STOCK MARKET MODULE (Yahoo Finance)
    # ============================================================
    def search_ticker(self, name):
        """Finds the ticker symbol dynamically (e.g. 'Zomato' -> 'ZOMATO.NS')"""
        url = "https://query2.finance.yahoo.com/v1/finance/search"
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            data = requests.get(url, params={'q': name, 'quotesCount': 1}, headers=headers).json()
            if 'quotes' in data and data['quotes']:
                # Prioritize Indian (.NS/.BO)
                for q in data['quotes']:
                    if q['symbol'].endswith(('.NS', '.BO')): return q['symbol']
                return data['quotes'][0]['symbol']
        except: pass
        return None

    def get_stock_metrics(self, symbol):
        """Fetches Price, PE, ROE, and News."""
        # 1. Resolve Name -> Symbol
        valid_symbol = symbol
        if not symbol.isupper() or "." not in symbol:
            found = self.search_ticker(symbol)
            if found: valid_symbol = found
            else: valid_symbol = f"{symbol.upper()}.NS"

        print(f"   📊 Fetching metrics for: {valid_symbol}")
        try:
            stock = yf.Ticker(valid_symbol)
            info = stock.info
            
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            if not price: return None

            return {
                "symbol": valid_symbol,
                "price": price,
                "currency": info.get('currency', 'INR'),
                "PE_Ratio": info.get('trailingPE', 'N/A'),
                "ROE": round((info.get('returnOnEquity', 0) or 0) * 100, 2),
                "Beta": info.get('beta', 'N/A'),
                "news_headline": self.search_web(f"{valid_symbol} stock analyst rating", 1)[0].get('title', 'No news')
            }
        except: return None

    def compare_stocks(self, tickers):
        return [self.get_stock_metrics(t) for t in tickers if self.get_stock_metrics(t)]

    def find_best_stock(self):
        return self.compare_stocks(self.default_watchlist)

    # ============================================================
    #  4. PROPERTY & INSURANCE (Search + Parse)
    # ============================================================
    def find_properties(self, location, max_budget=None):
        # We broaden the search to ensure results, then let the Brain filter by price
        query = f"2BHK flat for sale in {location} India price magicbricks 99acres"
        
        raw_data = self.search_web(query, max_results=5)
        # Pass to Gemini to clean up
        return self.clean_and_extract(raw_data, "property")

    def find_insurance(self, insurance_type, age, income):
        query = f"best {insurance_type} insurance plan India 2025 for {age} year old salary {income} review premiums policybazaar"
        
        raw_data = self.search_web(query, max_results=5)
        # Pass to Gemini to clean up
        return self.clean_and_extract(raw_data, "insurance")

    # ============================================================
    #  5. FORENSIC VERIFICATION (Anti-Scam)
    # ============================================================
    def verify_insurance_metrics(self, insurer_name):
        """Checks CSR/ASR ratios to detect bad insurers."""
        print(f"🕵️ AUDIT: Checking Claim Settlement Ratio for {insurer_name}...")
        
        query = f"{insurer_name} claim settlement ratio 2024 annual report amount settlement ratio"
        raw_results = self.search_web(query, max_results=3)
        
        prompt = f"""
        Extract Insurance Metrics for '{insurer_name}' from: {json.dumps(raw_results)}.
        FIND: CSR (Claim Settlement Ratio) and ASR (Amount Settlement Ratio).
        OUTPUT JSON: {{ "insurer": "{insurer_name}", "CSR": "XX%", "ASR": "XX%", "verdict": "SAFE/RISKY" }}
        """
        try:
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an Auditor. Output strictly valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                model=MODEL_NAME,
                response_format={"type": "json_object"}
            )
            return json.loads(completion.choices[0].message.content)
        except: return {"error": "Audit failed"}

    def verify_property_legality(self, project_name, location):
        """Checks RERA status."""
        print(f"🕵️ AUDIT: Checking RERA status for {project_name}...")
        
        query = f"{project_name} {location} RERA registration number complaints fraud legal issues"
        raw_results = self.search_web(query, max_results=3)
        
        prompt = f"""
        Analyze legal status for '{project_name}'.
        FIND: RERA ID, Legal Complaints, Possession Date issues.
        PORTALS: {json.dumps(self.rera_portals)}
        OUTPUT JSON: {{ "project": "{project_name}", "rera_id": "ID/NotFound", "legal_flags": ["list"], "check_here": "URL" }}
        """
        try:
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a Legal Auditor. Output strictly valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                model=MODEL_NAME,
                response_format={"type": "json_object"}
            )
            return json.loads(completion.choices[0].message.content)
        except: return {"error": "Audit failed"}