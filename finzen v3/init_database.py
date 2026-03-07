"""
Database Initialization Script for FinZen
Creates tables and populates with realistic synthetic user data
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, SessionLocal, Base
from app.db.models import User, Budget, Asset, Goal, Commitment, Transaction, Liability

def create_tables():
    """Create all database tables"""
    print("🔨 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

def clear_existing_data():
    """Clear existing data from all tables"""
    db = SessionLocal()
    try:
        print("🧹 Clearing existing data...")
        db.query(Transaction).delete()
        db.query(Commitment).delete()
        db.query(Goal).delete()
        db.query(Asset).delete()
        db.query(Budget).delete()
        db.query(Liability).delete()
        db.query(User).delete()
        db.commit()
        print("✅ Existing data cleared!")
    except Exception as e:
        print(f"⚠️ Error clearing data: {e}")
        db.rollback()
    finally:
        db.close()

def create_synthetic_users():
    """Create synthetic user profiles"""
    db = SessionLocal()
    try:
        print("👥 Creating synthetic users...")
        
        users_data = [
            {
                "id": 1,
                "username": "Siva Kumar",
                "email": "siva@finzen.com",
                "age": 28,
                "monthly_income": 85000,
                "emergency_fund_cash": 250000,
                "risk_tolerance": "Moderate",
                "is_investor": True,
                "alpaca_api_key": os.getenv("ALPACA_API_KEY"),
                "alpaca_secret_key": os.getenv("ALPACA_SECRET_KEY")
            },
            {
                "id": 2,
                "username": "Priya Sharma",
                "email": "priya@finzen.com",
                "age": 32,
                "monthly_income": 120000,
                "emergency_fund_cash": 500000,
                "risk_tolerance": "Conservative",
                "is_investor": True
            },
            {
                "id": 3,
                "username": "Rahul Verma",
                "email": "rahul@finzen.com",
                "age": 25,
                "monthly_income": 60000,
                "emergency_fund_cash": 100000,
                "risk_tolerance": "Aggressive",
                "is_investor": False
            }
        ]
        
        for user_data in users_data:
            user = User(**user_data)
            db.add(user)
        
        db.commit()
        print(f"✅ Created {len(users_data)} users!")
        return users_data
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
        return []
    finally:
        db.close()

def create_budgets(user_id=1):
    """Create budget categories for a user"""
    db = SessionLocal()
    try:
        print(f"💰 Creating budgets for user {user_id}...")
        
        budgets_data = [
            {"category": "Food", "limit_amount": 8000, "spent_so_far": 5200},
            {"category": "Travel", "limit_amount": 5000, "spent_so_far": 6500},  # Overspent
            {"category": "Rent", "limit_amount": 20000, "spent_so_far": 20000},
            {"category": "Entertainment", "limit_amount": 3000, "spent_so_far": 1800},
            {"category": "Shopping", "limit_amount": 5000, "spent_so_far": 5800},  # Overspent
            {"category": "Utilities", "limit_amount": 2000, "spent_so_far": 1500},
        ]
        
        for budget_data in budgets_data:
            budget = Budget(
                user_id=user_id,
                category=budget_data["category"],
                limit_amount=budget_data["limit_amount"],
                spent_so_far=budget_data["spent_so_far"]
            )
            db.add(budget)
        
        db.commit()
        print(f"✅ Created {len(budgets_data)} budget categories!")
    except Exception as e:
        print(f"❌ Error creating budgets: {e}")
        db.rollback()
    finally:
        db.close()

def create_assets(user_id=1):
    """Create investment assets for a user"""
    db = SessionLocal()
    try:
        print(f"📈 Creating assets for user {user_id}...")
        
        assets_data = [
            {
                "name": "RELIANCE",
                "asset_type": "Stock",
                "current_value": 25800.00,
                "growth_rate": 5.3
            },
            {
                "name": "TCS",
                "asset_type": "Stock",
                "current_value": 16750.00,
                "growth_rate": 4.7
            },
            {
                "name": "INFY",
                "asset_type": "Stock",
                "current_value": 22800.00,
                "growth_rate": 4.8
            },
            {
                "name": "Axis Bluechip Fund",
                "asset_type": "Mutual Fund",
                "current_value": 4820.00,
                "growth_rate": 5.9
            },
            {
                "name": "HDFC Index Fund",
                "asset_type": "Mutual Fund",
                "current_value": 10960.00,
                "growth_rate": 5.4
            }
        ]
        
        for asset_data in assets_data:
            asset = Asset(user_id=user_id, **asset_data)
            db.add(asset)
        
        db.commit()
        print(f"✅ Created {len(assets_data)} assets!")
    except Exception as e:
        print(f"❌ Error creating assets: {e}")
        db.rollback()
    finally:
        db.close()

def create_goals(user_id=1):
    """Create financial goals for a user"""
    db = SessionLocal()
    try:
        print(f"🎯 Creating goals for user {user_id}...")
        
        goals_data = [
            {
                "goal_name": "Emergency Fund",
                "target_amount": 500000,
                "current_saved_amount": 250000,
                "target_date": datetime.now() + timedelta(days=365),
                "priority_level": 1
            },
            {
                "goal_name": "Home Down Payment",
                "target_amount": 2000000,
                "current_saved_amount": 450000,
                "target_date": datetime.now() + timedelta(days=1095),  # 3 years
                "priority_level": 2
            },
            {
                "goal_name": "Vacation to Europe",
                "target_amount": 300000,
                "current_saved_amount": 80000,
                "target_date": datetime.now() + timedelta(days=180),
                "priority_level": 3
            }
        ]
        
        for goal_data in goals_data:
            goal = Goal(user_id=user_id, **goal_data)
            db.add(goal)
        
        db.commit()
        print(f"✅ Created {len(goals_data)} goals!")
    except Exception as e:
        print(f"❌ Error creating goals: {e}")
        db.rollback()
    finally:
        db.close()

def create_debts(user_id=1):
    """Create debt records for a user"""
    db = SessionLocal()
    try:
        print(f"💳 Creating debts for user {user_id}...")
        
        debts_data = [
            {
                "loan_type": "Home Loan",
                "remaining_balance": 2750000,
                "monthly_payment": 28500,
                "interest_rate": 8.5
            },
            {
                "loan_type": "Car Loan",
                "remaining_balance": 320000,
                "monthly_payment": 12000,
                "interest_rate": 9.0
            }
        ]
        
        for debt_data in debts_data:
            debt = Liability(user_id=user_id, **debt_data)
            db.add(debt)
        
        db.commit()
        print(f"✅ Created {len(debts_data)} debts!")
    except Exception as e:
        print(f"❌ Error creating debts: {e}")
        db.rollback()
    finally:
        db.close()

def create_transactions(user_id=1):
    """Create recent transactions for a user"""
    db = SessionLocal()
    try:
        print(f"💸 Creating transactions for user {user_id}...")
        
        transactions_data = [
            {"amount": -1200, "category": "Food", "description": "Grocery shopping at BigBasket"},
            {"amount": -2500, "category": "Travel", "description": "Uber rides this week"},
            {"amount": -800, "category": "Entertainment", "description": "Movie tickets and dinner"},
            {"amount": 85000, "category": "Salary", "description": "Monthly salary credit"},
            {"amount": -20000, "category": "Rent", "description": "Monthly rent payment"},
            {"amount": -5000, "category": "Investment", "description": "SIP in Mutual Fund"},
            {"amount": -1500, "category": "Shopping", "description": "Amazon purchase"},
            {"amount": -3200, "category": "Travel", "description": "Flight booking"},
        ]
        
        for i, tx_data in enumerate(transactions_data):
            transaction = Transaction(
                user_id=user_id,
                amount=tx_data["amount"],
                category=tx_data["category"],
                description=tx_data["description"],
                date=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.add(transaction)
        
        db.commit()
        print(f"✅ Created {len(transactions_data)} transactions!")
    except Exception as e:
        print(f"❌ Error creating transactions: {e}")
        db.rollback()
    finally:
        db.close()

def create_commitments(user_id=1):
    """Create recurring commitments for a user"""
    db = SessionLocal()
    try:
        print(f"📅 Creating commitments for user {user_id}...")
        
        commitments_data = [
            {
                "commitment_type": "Netflix Subscription",
                "amount": 649,
                "frequency": "Monthly",
                "next_due_date": datetime.now() + timedelta(days=15)
            },
            {
                "commitment_type": "Gym Membership",
                "amount": 1500,
                "frequency": "Monthly",
                "next_due_date": datetime.now() + timedelta(days=10)
            },
            {
                "commitment_type": "Life Insurance Premium",
                "amount": 15000,
                "frequency": "Yearly",
                "next_due_date": datetime.now() + timedelta(days=120)
            },
            {
                "commitment_type": "SIP - Mutual Fund",
                "amount": 5000,
                "frequency": "Monthly",
                "next_due_date": datetime.now() + timedelta(days=5)
            },
        ]
        
        for commitment_data in commitments_data:
            commitment = Commitment(user_id=user_id, **commitment_data)
            db.add(commitment)
        
        db.commit()
        print(f"✅ Created {len(commitments_data)} commitments!")
    except Exception as e:
        print(f"❌ Error creating commitments: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Main initialization function"""
    print("\n" + "="*60)
    print("🚀 FinZen Database Initialization")
    print("="*60 + "\n")
    
    # Create tables
    create_tables()
    
    # Clear existing data
    clear_existing_data()
    
    # Create synthetic data
    users = create_synthetic_users()
    
    if users:
        # Create data for the first user (primary test user)
        create_budgets(user_id=1)
        create_assets(user_id=1)
        create_goals(user_id=1)
        create_debts(user_id=1)
        create_transactions(user_id=1)
        create_commitments(user_id=1)
        
        print("\n" + "="*60)
        print("✅ Database initialization complete!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • Users created: {len(users)}")
        print(f"   • Primary user: {users[0]['username']} (ID: 1)")
        print(f"   • Monthly income: ₹{users[0]['monthly_income']:,}")
        print(f"   • Emergency fund: ₹{users[0]['emergency_fund_cash']:,}")
        print(f"   • Risk tolerance: {users[0]['risk_tolerance']}")
        print("\n💡 You can now start the API server with: python api.py")
        print("="*60 + "\n")
    else:
        print("\n❌ Failed to create users. Database initialization incomplete.")

if __name__ == "__main__":
    main()
