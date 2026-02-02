import sys
import json
from pathlib import Path
from datetime import datetime

# Add database to path
sys.path.append(str(Path(__file__).parent.parent / 'database'))

from db_config import get_session
from models import Transaction, User, TransactionCategory, FeeType, TransactionFee, SystemLog

def load_transactions_to_db(json_file_path):
    """Load parsed transactions from JSON into database"""
    
    # Read JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        transactions_data = json.load(f)
    
    session = get_session()
    
    try:
        # Get default user (first user in database)
        default_user = session.query(User).first()
        if not default_user:
            raise ValueError("No users in database. Run init_db.py first!")
        
        # Get category mappings
        categories = {cat.category_code: cat for cat in session.query(TransactionCategory).all()}
        
        # Get fee types
        transaction_fee_type = session.query(FeeType).filter_by(fee_name='Transaction Fee').first()
        if not transaction_fee_type:
            raise ValueError("Fee types not found. Run init_db.py first!")
        
        loaded_count = 0
        skipped_count = 0
        
        for trans_data in transactions_data:
            try:
                # Check if transaction already exists
                existing = session.query(Transaction).filter_by(
                    external_ref=trans_data['external_ref']
                ).first()
                
                if existing:
                    skipped_count += 1
                    continue
                
                # Map transaction type to category
                trans_type = trans_data.get('transaction_type', 'TRANSFER')
                category = categories.get(trans_type)
                if not category:
                    category = categories.get('TRANSFER')  # Default
                
                # Parse transaction date
                trans_date_str = trans_data.get('transaction_date')
                if trans_date_str:
                    trans_date = datetime.fromisoformat(trans_date_str)
                else:
                    trans_date = datetime.now()
                
                # Create transaction
                transaction = Transaction(
                    external_ref=trans_data['external_ref'],
                    amount=trans_data.get('amount', 0.0),
                    currency='RWF',
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
                if fee_amount >= 0:
                    fee = TransactionFee(
                        transaction_fee_amount=fee_amount,
                        created_at=datetime.now(),
                        transaction_id=transaction.transaction_id,
                        fee_type_id=transaction_fee_type.fee_type_id
                    )
                    session.add(fee)
                
                loaded_count += 1
                
            except Exception as e:
                print(f"Warning: Skipping transaction {trans_data.get('external_ref')}: {e}")
                skipped_count += 1
                continue
        
        # Commit all transactions
        session.commit()
        
        # Log to system logs
        log = SystemLog(
            log_type='BATCH_COMPLETE',
            severity='INFO',
            raw_sms_body=f'Loaded {loaded_count} transactions from {json_file_path}',
            log_time=datetime.now()
        )
        session.add(log)
        session.commit()
        
        print(f"✓ Successfully loaded {loaded_count} transactions")
        print(f"  Skipped {skipped_count} duplicate/invalid records")
        
    except Exception as e:
        session.rollback()
        print(f"✗ Error loading transactions: {e}")
        
        # Log error
        log = SystemLog(
            log_type='DB_ERROR',
            severity='ERROR',
            raw_sms_body=str(e),
            log_time=datetime.now()
        )
        session.add(log)
        session.commit()
        
        raise
    finally:
        session.close()

if __name__ == "__main__":
    json_file = "data/processed/parsed_sms.json"
    
    if not Path(json_file).exists():
        print(f"✗ File not found: {json_file}")
        print("  Run etl/parse_xml.py first!")
        sys.exit(1)
    
    print("Loading transactions into database...")
    load_transactions_to_db(json_file)
    print("\n✓ ETL process complete!")