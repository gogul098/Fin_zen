from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    
    # Financial Profile
    age = Column(Integer, default=30)
    occupation = Column(String, default="Professional")
    city_tier = Column(String, default="Tier 1")
    monthly_income = Column(Float, default=0.0)
    monthly_fixed_expenses = Column(Float, default=0.0)
    emergency_fund_cash = Column(Float, default=0.0)
    
    # Config
    risk_tolerance = Column(String, default="Moderate")
    alpaca_api_key = Column(String, nullable=True)
    alpaca_secret_key = Column(String, nullable=True)
    is_investor = Column(Boolean, default=False)

    # Relationships
    accounts = relationship("Account", back_populates="owner")
    debts = relationship("Liability", back_populates="owner")
    assets = relationship("Asset", back_populates="owner")
    goals = relationship("Goal", back_populates="owner")
    commitments = relationship("Commitment", back_populates="owner")
    transactions = relationship("Transaction", back_populates="owner")
    budgets = relationship("Budget", back_populates="owner")  # <--- Added Budget Relationship

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_type = Column(String)
    bank_name = Column(String)
    current_balance = Column(Float)
    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    amount = Column(Float)
    category = Column(String)
    description = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    asset_type = Column(String)
    name = Column(String)
    current_value = Column(Float)
    growth_rate = Column(Float)
    owner = relationship("User", back_populates="assets")

class Liability(Base): # Debts
    __tablename__ = "liabilities"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    loan_type = Column(String)
    remaining_balance = Column(Float)
    monthly_payment = Column(Float)
    interest_rate = Column(Float)
    owner = relationship("User", back_populates="debts")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    goal_name = Column(String)
    target_amount = Column(Float)
    current_saved_amount = Column(Float)
    target_date = Column(DateTime)
    priority_level = Column(Integer)
    owner = relationship("User", back_populates="goals")

class Commitment(Base): # Recurring Bills
    __tablename__ = "commitments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    commitment_type = Column(String)
    amount = Column(Float)
    frequency = Column(String)
    next_due_date = Column(DateTime)
    auto_pay_enabled = Column(Boolean, default=False)
    owner = relationship("User", back_populates="commitments")

# --- MISSING CLASS ADDED BELOW ---
class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String) # e.g. "Food", "Travel"
    limit_amount = Column(Float)
    spent_so_far = Column(Float, default=0.0)
    period = Column(String, default="Monthly")
    owner = relationship("User", back_populates="budgets")