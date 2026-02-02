import json
from pathlib import Path
from datetime import datetime
import re

def clean_normalize(sms_records):
    """
    Clean and normalize raw SMS data:
    - Convert timestamps to datetime
    - Normalize data types
    - Remove invalid records
    """
    cleaned_records = []
    skipped_count = 0
    
    for sms in sms_records:
        try:
            # Convert timestamp (milliseconds to datetime)
            if sms.get('date'):
                timestamp_ms = int(sms['date'])
                transaction_date = datetime.fromtimestamp(timestamp_ms / 1000)
            else:
                print(f"Warning: Missing date for SMS, skipping")
                skipped_count += 1
                continue
            
            # Convert type fields to integers
            sms_type = int(sms.get('type', 1))
            read_status = int(sms.get('read', 0))
            status = int(sms.get('status', -1))
            
            # Build cleaned record
            cleaned = {
                'address': sms.get('address'),
                'transaction_date': transaction_date.isoformat(),
                'transaction_date_readable': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
                'body': sms.get('body'),
                'service_center': sms.get('service_center'),
                'contact_name': sms.get('contact_name', '(Unknown)'),
                'type': sms_type,
                'read': read_status,
                'status': status,
            }
            
            cleaned_records.append(cleaned)
            
        except (ValueError, TypeError) as e:
            print(f"Warning: Skipping malformed record - {e}")
            skipped_count += 1
            continue
    
    print(f"✓ Cleaned {len(cleaned_records)} records")
    if skipped_count > 0:
        print(f"  Skipped {skipped_count} invalid records")
    
    return cleaned_records

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
    """Clean and normalize extracted data"""
    input_file = "../data/processed/01_extracted_raw.json"
    output_file = "../data/processed/02_cleaned_normalized.json"
    
    print("="*60)
    print("STEP 2: TRANSFORM - Clean & Normalize")
    print("="*60)
    
    try:
        # Load extracted data
        raw_data = load_from_json(input_file)
        print(f"Loaded {len(raw_data)} raw records")
        
        # Clean and normalize
        cleaned_data = clean_normalize(raw_data)
        
        # Save cleaned data
        save_to_json(cleaned_data, output_file)
        
        print(f"\nCleaning Summary:")
        print(f"   Input:  {input_file}")
        print(f"   Output: {output_file}")
        print(f"   Records: {len(cleaned_data)}")
        
    except Exception as e:
        print(f"✗ Cleaning failed: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
