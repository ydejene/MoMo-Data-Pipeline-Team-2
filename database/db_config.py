from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Database path
DATABASE_URL = 'sqlite:///database/db.sqlite3'

# Create engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debugging

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

def get_session():
    """Get a new database session"""
    return SessionLocal()