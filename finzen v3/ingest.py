import pandas as pd
import sys
import os

# Ensure we can import from the app folder
sys.path.append(os.getcwd())

from app.core.database import SessionLocal, engine, Base
from app.db.models import User, Transaction, Debt

# --- CONFIGURATION ---
CSV_FILE = "personal_finance.csv"

def ingest_profile_data():
    print("🗑️  Resetting Database for clean ingestion...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print(f"📂 Reading {CSV_FILE}...")
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{CSV_FILE}'. Please move it to the root folder.")
        return

    # --- PICK A "HERO" USER ---
    # We select the first row (Index 0) to be our active user for the demo.
    hero = df.iloc[0] 

    print(f"👤 Ingesting User Profile (Row 0):")
    print(f"   - Occupation: {hero['Occupation']}")
    print(f"   - Monthly Income: ₹{hero['Income']}")
    print(f"   - City Tier: {hero['City_Tier']}")

    # --- CALCULATE FINANCIALS ---
    monthly_income = float(hero['Income'])
    
    # 1. Calculate Fixed Expenses (Needs)
    # Summing up the non-negotiable bills from your CSV
    fixed_expenses = (
        float(hero['Rent']) + 
        float(hero['Loan_Repayment']) + 
        float(hero['Insurance']) + 
        float(hero['Utilities']) + 
        float(hero['Education']) +
        float(hero['Healthcare'])
    )

    # 2. Estimate Emergency Fund
    # If "Desired_Savings" is in the CSV, we assume they have 3 months of that saved.
    # Otherwise, we assume they have 10% of their annual income saved.
    desired_savings = float(hero.get('Desired_Savings', 0))
    if desired_savings == 0:
        emergency_fund = monthly_income * 2 # Fallback assumption
    else:
        emergency_fund = desired_savings * 3

    # --- CREATE USER IN DB ---
    user = User(
        username=f"User_{hero['Occupation']}",
        email="demo_user@finzen.ai",
        age=int(hero['Age']),
        occupation=hero['Occupation'],
        city_tier=hero['City_Tier'],
        monthly_income=monthly_income,
        monthly_fixed_expenses=fixed_expenses,
        emergency_fund_cash=emergency_fund,
        risk_tolerance="Moderate",
        is_investor=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # --- SYNTHESIZE TRANSACTIONS ---
    print("🚀 Converting Profile Columns into Transaction History...")
    
    tx_list = []
    
    # A. Add Income Transaction
    tx_list.append(Transaction(
        user_id=user.id, 
        amount=monthly_income, 
        category="Salary", 
        description="Monthly Occupation Income"
    ))

    # B. Map Expense Columns to Categories
    # Key = Your CSV Column Name | Value = Database Category
    expense_map = {
        "Rent": "Housing",
        "Groceries": "Food",
        "Transport": "Transport",
        "Eating_Out": "Dining",
        "Entertainment": "Entertainment",
        "Utilities": "Bills",
        "Healthcare": "Health",
        "Education": "Education",
        "Insurance": "Insurance",
        "Miscellaneous": "Misc"
    }

    for csv_col, db_cat in expense_map.items():
        if csv_col in hero and float(hero[csv_col]) > 0:
            amount = -float(hero[csv_col]) # Negative because it's spending
            tx_list.append(Transaction(
                user_id=user.id, 
                amount=amount, 
                category=db_cat, 
                description=f"{csv_col} Expense"
            ))

    db.add_all(tx_list)

    # --- ADD DEBT ---
    # Your CSV only gives "Loan_Repayment", not total debt.
    # We estimate Total Debt = Monthly Payment * 24 months (Standard rough estimate)
    if hero['Loan_Repayment'] > 0:
        total_estimated_debt = float(hero['Loan_Repayment']) * 24
        
        debt = Debt(
            user_id=user.id,
            name="Consolidated Loans",
            amount_remaining=total_estimated_debt,
            monthly_payment=float(hero['Loan_Repayment']),
            interest_rate=9.0 # Assumed average interest rate
        )
        db.add(debt)

    db.commit()
    print("✅ Ingestion Complete!")
    print(f"   -> Calculated Fixed Expenses: ₹{fixed_expenses:,.2f}")
    print(f"   -> Estimated Total Debt: ₹{total_estimated_debt:,.2f}" if hero['Loan_Repayment'] > 0 else "   -> No Debt Detected.")

if __name__ == "__main__":
    ingest_profile_data()