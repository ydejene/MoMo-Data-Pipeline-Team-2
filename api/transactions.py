"""
MoMo Transaction REST API Server
Provides CRUD endpoints for managing MoMo transaction data with Basic Authentication.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

# Import authentication helpers
from auth import is_authorized, send_unauthorized


class TransactionAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Transaction API with CRUD operations."""

    # In-memory storage
    transactions_list = []
    transactions_dict = {}
    next_id = 1

    # ---------- Helpers ----------

    def require_auth_or_return(self) -> bool:
        if not is_authorized(self.headers):
            send_unauthorized(self)
            return False
        return True

    def send_json_response(self, status_code: int, payload: dict | None = None):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if payload is not None:
            self.wfile.write(json.dumps(payload).encode("utf-8"))

    def read_json_body(self) -> dict | None:
        length = self.headers.get("Content-Length")
        if not length:
            return {}
        try:
            raw = self.rfile.read(int(length)).decode("utf-8")
            return json.loads(raw) if raw else {}
        except Exception:
            return None

    # ---------- HTTP Methods ----------

    def do_GET(self):
        if not self.require_auth_or_return():
            return

        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")

        if parts == ["transactions"]:
            self.get_all_transactions()
            return

        if len(parts) == 2 and parts[0] == "transactions":
            try:
                tx_id = int(parts[1])
            except ValueError:
                self.send_json_response(400, {"message": "Invalid transaction ID"})
                return
            self.get_transaction_by_id(tx_id)
            return

        self.send_json_response(404, {"message": "Endpoint not found"})

    def do_POST(self):
        if not self.require_auth_or_return():
            return

        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")

        if parts == ["transactions"]:
            body = self.read_json_body()
            if body is None:
                self.send_json_response(400, {"message": "Invalid JSON"})
                return
            self.create_transaction(body)
            return

        self.send_json_response(404, {"message": "Endpoint not found"})

    def do_PUT(self):
        if not self.require_auth_or_return():
            return

        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")

        if len(parts) == 2 and parts[0] == "transactions":
            try:
                tx_id = int(parts[1])
            except ValueError:
                self.send_json_response(400, {"message": "Invalid transaction ID"})
                return

            body = self.read_json_body()
            if body is None:
                self.send_json_response(400, {"message": "Invalid JSON"})
                return

            self.update_transaction(tx_id, body)
            return

        self.send_json_response(404, {"message": "Endpoint not found"})

    def do_DELETE(self):
        if not self.require_auth_or_return():
            return

        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")

        if len(parts) == 2 and parts[0] == "transactions":
            try:
                tx_id = int(parts[1])
            except ValueError:
                self.send_json_response(400, {"message": "Invalid transaction ID"})
                return

            self.delete_transaction(tx_id)
            return

        self.send_json_response(404, {"message": "Endpoint not found"})

    # ---------- CRUD Logic ----------

    def get_all_transactions(self):
        self.send_json_response(200, {
            "total_count": len(self.transactions_list),
            "transactions": self.transactions_list
        })

    def get_transaction_by_id(self, tx_id: int):
        tx = self.transactions_dict.get(tx_id)
        if not tx:
            self.send_json_response(404, {"message": "Transaction not found"})
            return
        self.send_json_response(200, tx)

    def create_transaction(self, data: dict):
        tx_id = self.next_id
        TransactionAPIHandler.next_id += 1

        tx = {"id": tx_id, **data}
        self.transactions_list.append(tx)
        self.transactions_dict[tx_id] = tx

        self.send_json_response(201, tx)

    def update_transaction(self, tx_id: int, data: dict):
        if tx_id not in self.transactions_dict:
            self.send_json_response(404, {"message": "Transaction not found"})
            return

        updated = {"id": tx_id, **data}
        self.transactions_dict[tx_id] = updated

        for i, item in enumerate(self.transactions_list):
            if item["id"] == tx_id:
                self.transactions_list[i] = updated
                break

        self.send_json_response(200, updated)

    def delete_transaction(self, tx_id: int):
        if tx_id not in self.transactions_dict:
            self.send_json_response(404, {"message": "Transaction not found"})
            return

        del self.transactions_dict[tx_id]
        self.transactions_list = [
            t for t in self.transactions_list if t["id"] != tx_id
        ]

        self.send_response(204)
        self.end_headers()


# ---------- Server bootstrap ----------

def seed_data():
    sample = [
        {"transaction_type": "RECEIVED", "amount": 5000, "currency": "RWF", "sender_name": "Alice"},
        {"transaction_type": "WITHDRAWN", "amount": 2000, "currency": "RWF", "receiver_name": "Bob"},
        {"transaction_type": "TRANSFER", "amount": 750, "currency": "RWF", "sender_name": "Carol", "receiver_name": "Dan"},
    ]

    for tx in sample:
        tx_id = TransactionAPIHandler.next_id
        TransactionAPIHandler.next_id += 1
        obj = {"id": tx_id, **tx}
        TransactionAPIHandler.transactions_list.append(obj)
        TransactionAPIHandler.transactions_dict[tx_id] = obj


def run_server():
    seed_data()
    server = HTTPServer(("localhost", 8000), TransactionAPIHandler)
    print("Server running on http://localhost:8000")
    print("Auth: admin:password123")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
