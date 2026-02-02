import sys
import json
from pathlib import Path
from datetime import datetime

# Add database to path
sys.path.append(str(Path(__file__).parent.parent / 'database'))

from db_config import get_session
from models import Transaction, User, TransactionCategory, FeeType, TransactionFee, SystemLog

def load_transactions_to_db(json_file_path):
    """Load categorized transactions into database"""
    
    # Read JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        transactions_data = json.load(f)
    
    session = get_session()
    
    try:
        # Get default user
        default_user = session.query(User).first()
        if not default_user:
            raise ValueError("No users found. Run database/init_db.py first!")
        
        # Get category mappings
        categories = {cat.category_code: cat for cat in session.query(TransactionCategory).all()}
        if not categories:
            raise ValueError("No categories found. Run database/init_db.py first!")
        
        # Get fee type
        transaction_fee_type = session.query(FeeType).filter_by(fee_name='Transaction Fee').first()
        if not transaction_fee_type:
            raise ValueError("Fee types not found. Run database/init_db.py first!")
        
        loaded_count = 0
        skipped_count = 0
        
        for trans_data in transactions_data:
            try:
                # Check if transaction already exists
                existing = session.query(Transaction).filter_by(
                    external_ref=trans_data['external_ref']
                ).first()
                
                if existing:
                    print(f"  Skipping duplicate: {trans_data['external_ref']}")
                    skipped_count += 1
                    continue
                
                # Get category
                category_code = trans_data.get('category_code', 'TRANSFER')
                category = categories.get(category_code, categories.get('TRANSFER'))
                
                # Parse transaction date
                trans_date = datetime.fromisoformat(trans_data['transaction_date'])
                
                # Create transaction
                transaction = Transaction(
                    external_ref=trans_data['external_ref'],
                    amount=trans_data.get('amount', 0.0),
                    currency=trans_data.get('currency', 'RWF'),
                    transaction_status=trans_data.get('transaction_status', 'COMPLETED'),
                    sender_notes=trans_data.get('subject'),
                    raw_data=trans_data['body'],
                    transaction_date=trans_date,
                    counter_party=trans_data.get('counter_party', 'Unknown'),
                    created_at=datetime.now(),
                    category_id=category.category_id,
                    user_id=default_user.user_id
                )
                
                session.add(transaction)
                session.flush()  # Get transaction_id
                
                # Add fee if present
                fee_amount = trans_data.get('fee_amount', 0.0)
                fee = TransactionFee(
                    transaction_fee_amount=fee_amount,
                    created_at=datetime.now(),
                    transaction_id=transaction.transaction_id,
                    fee_type_id=transaction_fee_type.fee_type_id
                )
                session.add(fee)
                
                loaded_count += 1
                
                if loaded_count % 10 == 0:
                    print(f"  Loaded {loaded_count} transactions...")
                
            except Exception as e:
                print(f"Warning: Skipping transaction {trans_data.get('external_ref')}: {e}")
                skipped_count += 1
                continue
        
        # Commit all
        session.commit()
        
        # Log success
        log = SystemLog(
            log_type='BATCH_COMPLETE',
            severity='INFO',
            raw_sms_body=f'Loaded {loaded_count} transactions, skipped {skipped_count}',
            log_time=datetime.now()
        )
        session.add(log)
        session.commit()
        
        print(f"\n✓ Successfully loaded {loaded_count} transactions to database")
        print(f"  Skipped {skipped_count} duplicate/invalid records")
        
        return loaded_count
        
    except Exception as e:
        session.rollback()
        
        # Log error
        log = SystemLog(
            log_type='DB_ERROR',
            severity='ERROR',
            raw_sms_body=str(e),
            log_time=datetime.now()
        )
        session.add(log)
        session.commit()
        
        print(f"✗ Error loading transactions: {e}")
        raise
        
    finally:
        session.close()

def main():
    """Load categorized transactions into database"""
    input_file = "../data/processed/03_categorized.json"
    
    print("="*60)
    print("STEP 4: LOAD - Save to Database")
    print("="*60)
    
    if not Path(input_file).exists():
        print(f"✗ File not found: {input_file}")
        print("  Run etl/categorize.py first!")
        sys.exit(1)
    
    try:
        loaded_count = load_transactions_to_db(input_file)
        
        print(f"\nLoad Summary:")
        print(f"   Input: {input_file}")
        print(f"   Database: database/db.sqlite3")
        print(f"   Loaded: {loaded_count} transactions")
        
    except Exception as e:
        print(f"✗ Load failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()