from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL - Use local SQLite for development, or cloud PostgreSQL from .env
# Default to SQLite if no DB_URL is provided
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DB_URL", 
    "sqlite:///./finzen_local.db"
)

# Create the Engine
print(f"🔌 Connecting to Database: {SQLALCHEMY_DATABASE_URL}")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# Create Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base
Base = declarative_base()