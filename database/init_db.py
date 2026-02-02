from db_config import init_db, get_session, drop_all_tables
from models import User, TransactionCategory, FeeType
from datetime import datetime

def seed_data():
    """Insert initial reference data"""
    session = get_session()
    
    try:
        # Seed Transaction Categories
        categories = [
            {'category_name': 'Transfer', 'category_code': 'TRANSFER', 'is_active': True},
            {'category_name': 'Payment', 'category_code': 'PAYMENT', 'is_active': True},
            {'category_name': 'Deposit', 'category_code': 'DEPOSIT', 'is_active': True},
            {'category_name': 'Withdrawal', 'category_code': 'WITHDRAWAL', 'is_active': True},
            {'category_name': 'Airtime Purchase', 'category_code': 'AIRTIME', 'is_active': True},
            {'category_name': 'Bill Payment', 'category_code': 'BILL_PAYMENT', 'is_active': True},
        ]
        
        for cat_data in categories:
            category = TransactionCategory(**cat_data)
            session.add(category)
        
        # Seed Fee Types
        fee_types = [
            {'fee_name': 'Transaction Fee'},
            {'fee_name': 'Tax'},
            {'fee_name': 'Service Charge'},
            {'fee_name': 'Agent Commission'},
            {'fee_name': 'Processing Fee'},
        ]
        
        for fee_data in fee_types:
            fee_type = FeeType(**fee_data)
            session.add(fee_type)
        
        # Create test users for API authentication
        users = [
            {
                'full_name': 'Admin User',
                'phone_number': '250788999999',
                'username': 'admin',
                'password_text': 'password123',
                'email_address': 'admin@momo.com',
                'created_at': datetime.now()
            },
            {
                'full_name': 'Test User',
                'phone_number': '250788888888',
                'username': 'testuser',
                'password_text': 'test123',
                'email_address': 'test@momo.com',
                'created_at': datetime.now()
            }
        ]
        
        for user_data in users:
            user = User(**user_data)
            session.add(user)
        
        session.commit()
        print("✓ Seed data inserted:")
        print(f"  - {len(categories)} transaction categories")
        print(f"  - {len(fee_types)} fee types")
        print(f"  - {len(users)} test users")
        
    except Exception as e:
        session.rollback()
        print(f"✗ Error seeding data: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    import sys
    
    # Optional: Drop existing tables
    if '--reset' in sys.argv:
        print("Dropping existing tables...")
        drop_all_tables()
    
    print("Creating database tables...")
    init_db()
    
    print("\nInserting seed data...")
    seed_data()
    
    print("\n✓ Database initialization complete!")
    print("  Location: database/db.sqlite3")
    print("\nTest credentials:")
    print("  Username: admin")
    print("  Password: password123")