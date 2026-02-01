import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET


def _parse_amount(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    return float(value.replace(",", ""))


def _parse_readable_date(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        dt = datetime.strptime(value, "%d %b %Y %I:%M:%S %p")
        return dt.isoformat()
    except ValueError:
        return value


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
            "readable_date_iso": _parse_readable_date(attributes.get("readable_date")),
            "status": attributes.get("status"),
            "read": attributes.get("read"),
            "locked": attributes.get("locked"),
            "service_center": attributes.get("service_center"),
            "contact_name": attributes.get("contact_name"),
        }

        transactions.append(transaction)

    return transactions


def save_transactions_to_json(transactions: List[Dict[str, Any]], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.write_text(json.dumps(transactions, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    default_xml = Path(__file__).resolve().parents[1] / "data" / "raw" / "modified_sms_v2.xml"
    default_out = Path(__file__).resolve().parents[1] / "data" / "processed" / "transactions.json"

    transactions = parse_sms_xml(default_xml)
    save_transactions_to_json(transactions, default_out)
    print(f"Successfully parsed {len(transactions)} transactions and saved to transactions.json!")