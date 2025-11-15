import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuration
DATABASE_FILE = "ble_visibility_map.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Creating SQLalchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# CreatingSessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class 
Base = declarative_base()

def get_db():
    """Dependency to get a database session for FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    """Creates database file and all defined tables."""
    if not os.path.exists(DATABASE_FILE):
        print(f"Creating database file: {DATABASE_FILE}")
    
    # Create all tables defined in Base's metadata (from models.py)
    Base.metadata.create_all(bind=engine)
    print("Database tables created/checked.")