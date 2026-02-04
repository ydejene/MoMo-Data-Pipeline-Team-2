from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

# Get the database directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Helper functions: Create/Drop DBs
def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print(f"✓ Database created at: {DATABASE_PATH}")

def get_session():
    """Get a new database session"""
    return SessionLocal()

def drop_all_tables():
    """Drop all tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
    print("✓ All tables dropped")