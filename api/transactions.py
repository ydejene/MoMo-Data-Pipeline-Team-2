"""
MoMo Transaction REST API Server
Provides CRUD endpoints for managing MoMo transaction data with Basic Authentication.

Endpoints:
- GET    /transactions
- GET    /transactions/{id}
- POST   /transactions
- PUT    /transactions/{id}
- DELETE /transactions/{id}

Auth:
- Basic Auth required for all endpoints
- Default credentials: admin:password123
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import base64


class TransactionAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Transaction API with CRUD operations."""

    # Class-level storage (shared across all requests)
    transactions_list = []
    transactions_dict = {}
    next_id = 1

    # -------------------------
    # Core helpers
    # -------------------------

    def send_json_response(self, status_code: int, payload: dict | None = None) -> None:
        """Send JSON response with status code."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if payload is not None:
            self.wfile.write(json.dumps(payload).encode("utf-8"))

    def read_json_body(self) -> dict | None:
        """Read and parse JSON request body. Returns dict or None if invalid."""
        length = self.headers.get("Content-Length")
        if not length:
            return {}
        try:
            raw = self.rfile.read(int(length)).decode("utf-8")
            if raw.strip() == "":
                return {}
            return json.loads(raw)
        except Exception:
            return None

    def check_authentication(self) -> bool:
        """
        Check if request has valid Basic Auth credentials.
        Expected header: Authorization: Basic base64(username:password)
        """
        auth_header = self.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Basic "):
            return False

        encoded = auth_header.split(" ", 1)[1].strip()
        try:
            decoded = base64.b64decode(encoded).decode("utf-8")
        except Exception:
            return False

        if ":" not in decoded:
            return False

        username, password = decoded.split(":", 1)

        # Hardcoded credentials for assignment
        return username == "admin" and password == "password123"

    def send_unauthorized(self) -> None:
        """Return 401 Unauthorized with WWW-Authenticate header."""
        self.send_response(401)
        self.send_header("Content-Type", "application/json")
        self.send_header("WWW-Authenticate", 'Basic realm="MoMo API"')
        self.end_headers()
        payload = {
            "status": "error",
            "message": "Unauthorized. Provide valid Basic Authentication credentials.",
            "error_code": "UNAUTHORIZED",
        }
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def require_auth_or_return(self) -> bool:
        """Return True if authorized, else send 401 and return False."""
        if not self.check_authentication():
            self.send_unauthorized()
            return False
        return True

    # -------------------------
    # Routing
    # -------------------------

    def do_GET(self):
        if not self.require_auth_or_return():
            return

        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        # GET /transactions
        if len(path_parts) == 1 and path_parts[0] == "transactions":
            self.get_all_transactions()
            return

        # GET /transactions/{id}
        if len(path_parts) == 2 and path_parts[0] == "transactions":
            try:
                transaction_id = int(path_parts[1])
            except ValueError:
                self.send_json_response(400, {
                    "status": "error",
                    "message": "Invalid transaction ID",
                    "error_code": "INVALID_ID",
                })
                return
            self.get_transaction_by_id(transaction_id)
            return

        self.send_json_response(404, {
            "status": "error",
            "message": "Endpoint not found",
            "error_code": "NOT_FOUND",
        })

    def do_POST(self):
        if not self.require_auth_or_return():
            return

        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        # POST /transactions
        if len(path_parts) == 1 and path_parts[0] == "transactions":
            body = self.read_json_body()
            if body is None:
                self.send_json_response(400, {
                    "status": "error",
                    "message": "Invalid JSON body",
                    "error_code": "INVALID_JSON",
                })
                return

            self.create_transaction(body)
            return

        self.send_json_response(404, {
            "status": "error",
            "message": "Endpoint not found",
            "error_code": "NOT_FOUND",
        })

    def do_PUT(self):
        if not self.require_auth_or_return():
            return

        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        # PUT /transactions/{id}
        if len(path_parts) == 2 and path_parts[0] == "transactions":
            try:
                transaction_id = int(path_parts[1])
            except ValueError:
                self.send_json_response(400, {
                    "status": "error",
                    "message": "Invalid transaction ID",
                    "error_code": "INVALID_ID",
                })
                return

            body = self.read_json_body()
            if body is None:
                self.send_json_response(400, {
                    "status": "error",
                    "message": "Invalid JSON body",
                    "error_code": "INVALID_JSON",
                })
                return

            self.update_transaction(transaction_id, body)
            return

        self.send_json_response(404, {
            "status": "error",
            "message": "Endpoint not found",
            "error_code": "NOT_FOUND",
        })

    def do_DELETE(self):
        if not self.require_auth_or_return():
            return

        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        # DELETE /transactions/{id}
        if len(path_parts) == 2 and path_parts[0] == "transactions":
            try:
                transaction_id = int(path_parts[1])
            except ValueError:
                self.send_json_response(400, {
                    "status": "error",
                    "message": "Invalid transaction ID",
                    "error_code": "INVALID_ID",
                })
                return

            self.delete_transaction_by_id(transaction_id)
            return

        self.send_json_response(404, {
            "status": "error",
            "message": "Endpoint not found",
            "error_code": "NOT_FOUND",
        })

    def do_PATCH(self):
        self.send_json_response(405, {
            "status": "error",
            "message": "Method not allowed",
            "error_code": "METHOD_NOT_ALLOWED",
        })

    # -------------------------
    # CRUD logic
    # -------------------------

    def get_all_transactions(self):
        self.send_json_response(200, {
            "status": "success",
            "message": "Transactions retrieved successfully",
            "data": {
                "total_count": len(self.transactions_list),
                "transactions": self.transactions_list,
            },
        })

    def get_transaction_by_id(self, transaction_id: int):
        # Dict lookup (O(1))
        tx = self.transactions_dict.get(transaction_id)
        if not tx:
            self.send_json_response(404, {
                "status": "error",
                "message": f"Transaction with ID {transaction_id} not found",
                "error_code": "TRANSACTION_NOT_FOUND",
            })
            return

        self.send_json_response(200, {
            "status": "success",
            "message": "Transaction retrieved successfully",
            "data": tx,
        })

    def create_transaction(self, data: dict):
        # Generate ID
        tx_id = self.next_id
        TransactionAPIHandler.next_id += 1

        # Create transaction object (store raw + id)
        tx = {"id": tx_id, **data}

        TransactionAPIHandler.transactions_list.append(tx)
        TransactionAPIHandler.transactions_dict[tx_id] = tx

        self.send_json_response(201, {
            "status": "success",
            "message": "Transaction created successfully",
            "data": tx,
        })

    def update_transaction(self, transaction_id: int, data: dict):
        existing = self.transactions_dict.get(transaction_id)
        if not existing:
            self.send_json_response(404, {
                "status": "error",
                "message": f"Transaction with ID {transaction_id} not found",
                "error_code": "TRANSACTION_NOT_FOUND",
            })
            return

        # Update fields (keep id fixed)
        updated = {"id": transaction_id, **data}

        # Update dict
        TransactionAPIHandler.transactions_dict[transaction_id] = updated

        # Update list
        for i, item in enumerate(TransactionAPIHandler.transactions_list):
            if item.get("id") == transaction_id:
                TransactionAPIHandler.transactions_list[i] = updated
                break

        self.send_json_response(200, {
            "status": "success",
            "message": "Transaction updated successfully",
            "data": updated,
        })

    def delete_transaction_by_id(self, transaction_id: int):
        existing = self.transactions_dict.get(transaction_id)
        if not existing:
            self.send_json_response(404, {
                "status": "error",
                "message": f"Transaction with ID {transaction_id} not found",
                "error_code": "TRANSACTION_NOT_FOUND",
            })
            return

        # Remove from dict
        del TransactionAPIHandler.transactions_dict[transaction_id]

        # Remove from list
        TransactionAPIHandler.transactions_list = [
            tx for tx in TransactionAPIHandler.transactions_list
            if tx.get("id") != transaction_id
        ]

        # 204 No Content
        self.send_response(204)
        self.end_headers()


def seed_data():
    """Add a few transactions so GET/DELETE testing works immediately."""
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


def run_server(host: str = "localhost", port: int = 8000):
    seed_data()
    server = HTTPServer((host, port), TransactionAPIHandler)
    print(f"Server running on http://{host}:{port}")
    print("Auth: admin:password123")
    print("Try: curl -i -u admin:password123 http://localhost:8000/transactions")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
