import json
from pathlib import Path
import re

def extract_transaction_details(body):
    """Extract transaction details from SMS body"""
    details = {}
    
    # Extract transaction ID
    txid_patterns = [
        r'TxId:\s*(\d+)',
        r'Transaction Id:\s*(\d+)',
        r'Financial Transaction Id:\s*(\d+)'
    ]
    for pattern in txid_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            details['external_ref'] = match.group(1)
            break
    
    # Extract amount (remove commas, convert to float)
    amount_pattern = r'(\d+(?:,\d+)(?:\.\d+)?)\sRWF'
    match = re.search(amount_pattern, body)
    if match:
        amount_str = match.group(1).replace(',', '')
        details['amount'] = float(amount_str)
    else:
        details['amount'] = 0.0
    
    # Extract counter party (other person's name)
    name_patterns = [
        r'from\s+([\w\s]+?)\s+\(',
        r'to\s+([\w\s]+?)\s+\d',
        r'from\s+([\w\s]+?)\s+\*',
    ]
    for pattern in name_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            details['counter_party'] = match.group(1).strip()
            break
    
    if 'counter_party' not in details:
        details['counter_party'] = 'Unknown'
    
    # Extract fee
    fee_pattern = r'Fee was (\d+(?:\.\d+)?)\s*RWF'
    match = re.search(fee_pattern, body, re.IGNORECASE)
    if match:
        details['fee_amount'] = float(match.group(1))
    else:
        details['fee_amount'] = 0.0
    
    return details

def categorize_transaction(body):
    """
    Determine transaction category based on SMS body keywords
    Returns category_code
    """
    body_lower = body.lower()
    
    # Categorization rules
    if 'received' in body_lower or 'sent' in body_lower:
        return 'TRANSFER'
    elif 'payment' in body_lower or 'paid' in body_lower:
        return 'PAYMENT'
    elif 'deposit' in body_lower or 'added to your' in body_lower:
        return 'DEPOSIT'
    elif 'withdraw' in body_lower or 'withdrawn' in body_lower:
        return 'WITHDRAWAL'
    elif 'airtime' in body_lower:
        return 'AIRTIME'
    elif 'bill' in body_lower or 'utility' in body_lower:
        return 'BILL_PAYMENT'
    else:
        return 'TRANSFER'  # Default

def determine_status(body):
    """Determine transaction status from SMS body"""
    body_lower = body.lower()
    
    if 'failed' in body_lower or 'unsuccessful' in body_lower:
        return 'FAILED'
    elif 'pending' in body_lower:
        return 'PENDING'
    else:
        return 'COMPLETED'

def categorize_records(cleaned_records):
    """Add category and extract transaction details"""
    categorized_records = []
    skipped_count = 0
    
    for record in cleaned_records:
        body = record.get('body', '')
        
        # Extract transaction details
        details = extract_transaction_details(body)
        
        # Skip if no transaction ID found (not a transaction SMS)
        if 'external_ref' not in details:
            skipped_count += 1
            continue
        
        # Add categorization
        category_code = categorize_transaction(body)
        status = determine_status(body)
        
        # Build categorized record
        categorized = {
            **record,  # Keep all cleaned fields
            'external_ref': details['external_ref'],
            'amount': details['amount'],
            'counter_party': details['counter_party'],
            'fee_amount': details['fee_amount'],
            'category_code': category_code,
            'transaction_status': status,
            'currency': 'RWF'  # Default currency
        }
        
        categorized_records.append(categorized)
    
    print(f"✓ Categorized {len(categorized_records)} transactions")
    if skipped_count > 0:
        print(f"  Skipped {skipped_count} non-transaction messages")
    
    return categorized_records

def load_from_json(file_path):
    """Load data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_to_json(data, output_path):
    """Save data to JSON file"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved to {output_path}")

def main():
    """Categorize cleaned transactions"""
    input_file = "../data/processed/02_cleaned_normalized.json"
    output_file = "../data/processed/03_categorized.json"
    
    print("="*60)
    print("STEP 3: TRANSFORM - Categorize Transactions")
    print("="*60)
    
    try:
        # Load cleaned data
        cleaned_data = load_from_json(input_file)
        print(f"Loaded {len(cleaned_data)} cleaned records")
        
        # Categorize
        categorized_data = categorize_records(cleaned_data)
        
        # Save categorized data
        save_to_json(categorized_data, output_file)
        
        # Show category distribution
        category_counts = {}
        for record in categorized_data:
            cat = record.get('category_code', 'UNKNOWN')
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        print(f"\nCategorization Summary:")
        print(f"   Input:  {input_file}")
        print(f"   Output: {output_file}")
        print(f"   Total transactions: {len(categorized_data)}")
        print(f"\n   Category breakdown:")
        for cat, count in sorted(category_counts.items()):
            print(f"     - {cat}: {count}")
        
    except Exception as e:
        print(f"✗ Categorization failed: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()