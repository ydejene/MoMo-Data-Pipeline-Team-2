import json
from pathlib import Path
from typing import Any, Dict, List
from xml.etree import ElementTree as ET


def parse_sms_xml(file_path: str | Path) -> List[Dict[str, Any]]:
    file_path = Path(file_path)
    tree = ET.parse(file_path)
    root = tree.getroot()

    transactions: List[Dict[str, Any]] = []

    for idx, sms in enumerate(root.findall("sms"), start=1):
        attributes = sms.attrib
        body = attributes.get("body", "")

        transaction = {
            "id": attributes.get("date", str(idx)),
            "index": idx,
            "address": attributes.get("address"),
            "protocol": attributes.get("protocol"),
            "type": attributes.get("type"),
            "subject": attributes.get("subject"),
            "raw_body": body,
            "date": attributes.get("date"),
            "readable_date": attributes.get("readable_date"),
            "status": attributes.get("status"),
            "read": attributes.get("read"),
            "locked": attributes.get("locked"),
            "service_center": attributes.get("service_center"),
            "contact_name": attributes.get("contact_name"),
        }

        transactions.append(transaction)

    return transactions


if __name__ == "__main__":
    default_xml = Path(__file__).resolve().parents[1] / "data" / "raw" / "modified_sms_v2.xml"
    
    transactions = parse_sms_xml(default_xml)
    print(f"Parsed {len(transactions)} transactions from XML")