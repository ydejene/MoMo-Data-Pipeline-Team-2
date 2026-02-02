import xml.etree.ElementTree as ET
from datetime import datetime
import json
from pathlib import Path

def parse_xml(file_path):
    """
    Extract raw SMS data from XML file.
    NO transformation - just extraction.
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"XML file not found: {file_path}")
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        raise ET.ParseError(f"Invalid XML format: {e}")
    
    sms_list = []
    
    for sms_element in root.findall('sms'):
        # Extract raw attributes - NO PROCESSING
        date_raw = sms_element.get('date')
        
        sms_dict = {
            'protocol': sms_element.get('protocol'),
            'address': sms_element.get('address'),
            'date': date_raw,  # Keep as string
            'type': sms_element.get('type'),
            'subject': sms_element.get('subject'),
            'body': sms_element.get('body'),
            'toa': sms_element.get('toa'),
            'sc_toa': sms_element.get('sc_toa'),
            'service_center': sms_element.get('service_center'),
            'read': sms_element.get('read'),
            'status': sms_element.get('status'),
            'locked': sms_element.get('locked'),
            'date_sent': sms_element.get('date_sent'),
            'sub_id': sms_element.get('sub_id'),
            'readable_date': sms_element.get('readable_date'),
            'contact_name': sms_element.get('contact_name')
        }
        
        # Only include if it's an M-Money message
        if sms_dict.get('address') == 'M-Money' and sms_dict.get('body'):
            sms_list.append(sms_dict)
    
    print(f"✓ Extracted {len(sms_list)} M-Money SMS records")
    return sms_list

def save_to_json(data, output_path):
    """Save extracted data to JSON"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved to {output_path}")

def main():
    """Extract raw SMS data from XML"""
    input_file = "../data/raw/modified_sms_v2.xml"
    output_file = "../data/processed/01_extracted_raw.json"
    
    print("="*60)
    print("STEP 1: EXTRACT - Parsing XML")
    print("="*60)
    
    try:
        sms_records = parse_xml(input_file)
        save_to_json(sms_records, output_file)
        
        print(f"\n📊 Extraction Summary:")
        print(f"   Input:  {input_file}")
        print(f"   Output: {output_file}")
        print(f"   Records: {len(sms_records)}")
        
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()