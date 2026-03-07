import sys
import os
import json
import pdfplumber
from groq import Groq
from datetime import datetime
from dotenv import load_dotenv

# Ensure we can import from the app folder
sys.path.append(os.getcwd())

from app.core.database import SessionLocal, engine, Base
from app.db.models import User, Transaction

# Load env vars
load_dotenv()

# Configure Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("❌ Error: GROQ_API_KEY not found in .env")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama3-70b-8192"

def extract_text_from_pdf(pdf_path):
    """Extracts raw text from a PDF file."""
    print(f"📄 Reading PDF: {pdf_path}...")
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        return full_text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

def parse_with_llm(raw_text):
    """Uses Groq (Llama 3) to extract structured transactions and financial context while sanitizing PII."""
    print("🤖 Analyzing text with Llama 3 (Privacy Filter Active)...")
    
    prompt = """
    You are a strictly compliant Data Extraction AI.
    
    TASK:
    Analyze the following Bank Statement text and extract:
    1. A list of Transactions (Date, Description, Amount, Category).
    2. A summary of the financial profile (Monthly Income, Fixed Expenses estimate).
    
    PRIVACY RULES (CRITICAL):
    - DO NOT extract Names, Addresses, Account Numbers, Phone Numbers, or Email Addresses.
    - If you see a Name or Address, IGNORE IT.
    - The output must be purely quantitative and categorical.
    - Dates should be in format YYYY-MM-DD.
    - Amounts: Negative for debit/expense, Positive for credit/income.
    
    OUTPUT FORMAT (JSON ONLY):
    {
        "transactions": [
            {"date": "YYYY-MM-DD", "description": "Short desc", "amount": -50.00, "category": "Food/Travel/Rent/etc"}
        ],
        "profile_summary": {
            "estimated_income": 0.0,
            "estimated_fixed_expenses": 0.0,
            "currency": "INR"
        }
    }
    
    INPUT TEXT:
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a JSON Extractor."},
                {"role": "user", "content": prompt + "\n" + raw_text}
            ],
            model=MODEL_NAME,
            response_format={"type": "json_object"}
        )
        
        data = json.loads(completion.choices[0].message.content)
        return data
    except Exception as e:
        print(f"❌ Error parsing with LLM: {e}")
        return None

def ingest_to_db(data, user_id=1):
    """Saves the extracted data to the database."""
    print("💾 Saving to Database...")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            print(f"❌ User ID {user_id} not found.")
            return

        # Update User Profile Estimates (optional, based on PDF analysis)
        summary = data.get("profile_summary", {})
        if summary.get("estimated_income", 0) > 0:
            print(f"   -> Updating User Income est: {summary['estimated_income']}")
            # user.monthly_income = summary['estimated_income'] # Uncomment to auto-update
            
        # Add Transactions
        count = 0
        for tx in data.get("transactions", []):
            transaction = Transaction(
                user_id=user.id,
                amount=tx['amount'],
                category=tx['category'],
                description=tx['description'],
                date=datetime.strptime(tx['date'], "%Y-%m-%d") if tx.get('date') else datetime.now()
            )
            db.add(transaction)
            count += 1
            
        db.commit()
        print(f"✅ Successfully added {count} anonymized transactions!")
        return count
        
    except Exception as e:
        print(f"❌ Database Error: {e}")
        db.rollback()
        return 0
    finally:
        db.close()


def process_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return 0

    # 1. Extract
    raw_text = extract_text_from_pdf(pdf_path)
    if not raw_text:
        return 0

    # 2. Parse & Anonymize
    structured_data = parse_with_llm(raw_text)
    if not structured_data:
        print("❌ Failed to parse data.")
        return 0

    # 3. Ingest
    count = ingest_to_db(structured_data)
    
    # 4. Cleanup (Privacy)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        print(f"🗑️ Securely deleted: {pdf_path}")

    return count

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest_pdf.py <path_to_bank_statement.pdf>")
    else:
        process_pdf(sys.argv[1])
