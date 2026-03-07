import random
from datetime import datetime, timedelta
from app.core.database import Base, engine, SessionLocal
from app.db.models import User, Account, Transaction, Asset, Liability, Goal, Commitment, Budget

# 1. Reset Database
print("🏭 REALISM FACTORY: Clearing Database...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# 2. Create Profile (The "Urban Professional")
print("👤 Creating Persona: Arjun...")
user = User(
    username="Arjun",
    email="arjun@finzen.ai",
    age=29,
    occupation="Product Manager",
    city_tier="Tier 1", # Mumbai/Bangalore costs
    monthly_income=145000.0,
    monthly_fixed_expenses=65000.0,
    emergency_fund_cash=120000.0, 
    risk_tolerance="Aggressive",
    is_investor=True
)
db.add(user)
db.commit()

# 3. Accounts
acc = Account(user_id=user.id, account_type="Savings", bank_name="HDFC Bank", current_balance=210450.0)
db.add(acc)
db.commit()

# 4. Assets & Debts
db.add_all([
    Asset(user_id=user.id, asset_type="Stock", name="TATA MOTORS", current_value=85000, growth_rate=14),
    Asset(user_id=user.id, asset_type="MF", name="Parag Parikh Flexi Cap", current_value=320000, growth_rate=12),
    Liability(user_id=user.id, loan_type="Personal Loan", remaining_balance=150000, monthly_payment=8500, interest_rate=11.0),
    Goal(user_id=user.id, goal_name="Europe Trip", target_amount=300000, current_saved_amount=60000, target_date=datetime(2025, 6, 1), priority_level=4)
])

# 5. Commitments (The "Must Pays")
db.add_all([
    Commitment(user_id=user.id, commitment_type="Rent", amount=35000, frequency="Monthly", next_due_date=datetime(2025, 12, 1)),
    Commitment(user_id=user.id, commitment_type="Maid & Cook", amount=6000, frequency="Monthly", next_due_date=datetime(2025, 12, 5)),
    Commitment(user_id=user.id, commitment_type="Wifi/Internet", amount=1200, frequency="Monthly", next_due_date=datetime(2025, 12, 10)),
    Commitment(user_id=user.id, commitment_type="Netflix & Spotify", amount=899, frequency="Monthly", next_due_date=datetime(2025, 12, 15))
])

# 6. BUDGETS (The "Diversified" Real Life Logic)
# We simulate that the user has already spent some money this month.
print("💰 Setting Realistic Budgets...")
budgets = [
    # Essentials
    Budget(user_id=user.id, category="Groceries", limit_amount=10000, spent_so_far=6500), # 65% used
    Budget(user_id=user.id, category="Transport (Uber/Metro)", limit_amount=8000, spent_so_far=7200), # Almost full
    Budget(user_id=user.id, category="Utilities", limit_amount=5000, spent_so_far=3500),
    
    # Lifestyle (The Problem Areas)
    Budget(user_id=user.id, category="Dining & Nightlife", limit_amount=12000, spent_so_far=11000), # Danger zone!
    Budget(user_id=user.id, category="Shopping", limit_amount=10000, spent_so_far=12500), # 🚨 OVER BUDGET!
    Budget(user_id=user.id, category="Self Care/Gym", limit_amount=3000, spent_so_far=1500),
    
    # Savings Goal
    Budget(user_id=user.id, category="Investments", limit_amount=30000, spent_so_far=20000)
]
db.add_all(budgets)
db.commit()

# 7. TRANSACTION SIMULATION (90 Days)
print("💸 Generating 90 Days of Chaos...")
start_date = datetime.now() - timedelta(days=90)
tx_list = []

# Merchant mapping for realism
merchants = {
    "Groceries": ["Blinkit", "Zepto", "D-Mart", "Local Kirana"],
    "Dining": ["Social", "Starbucks", "Dominos", "Chilis", "Zomato"],
    "Transport": ["Uber", "Ola", "Shell Petrol", "Rapido"],
    "Shopping": ["Myntra", "Amazon", "Uniqlo", "Zara", "Nykaa"],
    "Utilities": ["Bescom", "Jio Fiber", "Airtel Postpaid"],
    "Self Care": ["Urban Company", "Cult.fit", "Apollo Pharmacy"]
}

for i in range(90):
    curr_date = start_date + timedelta(days=i)
    is_weekend = curr_date.weekday() >= 5 
    
    # Salary
    if curr_date.day == 1:
        tx_list.append(Transaction(user_id=user.id, account_id=acc.id, amount=145000, category="Salary", description="Salary - TechCorp", date=curr_date))

    # Rent
    if curr_date.day == 5:
        tx_list.append(Transaction(user_id=user.id, account_id=acc.id, amount=-35000, category="Housing", description="Rent Transfer", date=curr_date))

    # Random Daily Spends
    if random.random() > 0.4: # Daily stuff
        cat = random.choice(["Groceries", "Transport"])
        merch = random.choice(merchants[cat])
        tx_list.append(Transaction(user_id=user.id, account_id=acc.id, amount=-random.randint(100, 800), category=cat, description=merch, date=curr_date))

    # Weekend Splurges
    if is_weekend and random.random() > 0.3:
        cat = random.choice(["Dining", "Shopping", "Self Care"])
        merch = random.choice(merchants[cat])
        amount = -random.randint(800, 5000) # Big spends
        tx_list.append(Transaction(user_id=user.id, account_id=acc.id, amount=amount, category=cat, description=merch, date=curr_date))

db.add_all(tx_list)
db.commit()
print("✅ Real-World Data Generated.")
print("   -> Note: User has OVERSPENT on Shopping (Used 12.5k of 10k budget).")
print("   -> The AI should be able to detect this!")