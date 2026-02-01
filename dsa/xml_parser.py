import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET


AMOUNT_RE = re.compile(r"(?P<amount>[0-9,]+)\s*RWF", re.IGNORECASE)
TXID_RE = re.compile(r"(?:TxId|Transaction Id|Financial Transaction Id|External Transaction Id)[:\s]+(?P<txid>[0-9]+)")

TRANSFER_RE = re.compile(r"transferred to\s+(?P<name>[^()]+)\s*\((?P<phone>[0-9*]+)\)", re.IGNORECASE)
PAYMENT_RE = re.compile(r"payment of\s+(?P<amount>[0-9,]+)\s*RWF\s+to\s+(?P<name>[^0-9]+)\s*(?P<code>[0-9]+)?", re.IGNORECASE)
RECEIVED_RE = re.compile(r"received\s+(?P<amount>[0-9,]+)\s*RWF\s+from\s+(?P<name>[^()]+)", re.IGNORECASE)
DEPOSIT_RE = re.compile(r"bank deposit of\s+(?P<amount>[0-9,]+)\s*RWF", re.IGNORECASE)
WITHDRAW_RE = re.compile(r"withdrawn\s+(?P<amount>[0-9,]+)\s*RWF", re.IGNORECASE)
FEE_RE = re.compile(r"Fee(?: was| paid| was:)\s*:?\s*(?P<fee>[0-9,]+)\s*RWF", re.IGNORECASE)
BALANCE_RE = re.compile(r"New balance:?\s*(?P<balance>[0-9,]+)\s*RWF", re.IGNORECASE)


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


def _extract_body_fields(body: str) -> Dict[str, Any]:
    """Extract transaction fields from SMS body text using regex patterns."""
    fields: Dict[str, Any] = {
        "transaction_type": None,
        "amount": None,
        "currency": "RWF",
        "sender_name": None,
        "receiver_name": None,
        "receiver_phone": None,
        "fee": None,
        "balance": None,
        "transaction_id": None,
    }

    txid_match = TXID_RE.search(body)
    if txid_match:
        fields["transaction_id"] = txid_match.group("txid")

    fee_match = FEE_RE.search(body)
    if fee_match:
        fields["fee"] = _parse_amount(fee_match.group("fee"))

    balance_match = BALANCE_RE.search(body)
    if balance_match:
        fields["balance"] = _parse_amount(balance_match.group("balance"))

    transfer_match = TRANSFER_RE.search(body)
    if transfer_match:
        fields["transaction_type"] = "TRANSFER"
        fields["receiver_name"] = transfer_match.group("name").strip()
        fields["receiver_phone"] = transfer_match.group("phone").replace("*", "")

    payment_match = PAYMENT_RE.search(body)
    if payment_match:
        fields["transaction_type"] = "PAYMENT"
        fields["amount"] = _parse_amount(payment_match.group("amount"))
        fields["receiver_name"] = payment_match.group("name").strip()

    received_match = RECEIVED_RE.search(body)
    if received_match:
        fields["transaction_type"] = "RECEIVED"
        fields["amount"] = _parse_amount(received_match.group("amount"))
        fields["sender_name"] = received_match.group("name").strip()

    deposit_match = DEPOSIT_RE.search(body)
    if deposit_match:
        fields["transaction_type"] = "DEPOSIT"
        fields["amount"] = _parse_amount(deposit_match.group("amount"))

    withdraw_match = WITHDRAW_RE.search(body)
    if withdraw_match:
        fields["transaction_type"] = "WITHDRAWAL"
        fields["amount"] = _parse_amount(withdraw_match.group("amount"))

    if fields["amount"] is None:
        amount_match = AMOUNT_RE.search(body)
        if amount_match:
            fields["amount"] = _parse_amount(amount_match.group("amount"))

    return fields


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