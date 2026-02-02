# api/auth.py
import base64
import json
from typing import Tuple


DEFAULT_REALM = "MoMo API"


def _parse_basic_header(auth_header: str) -> Tuple[str | None, str | None]:
    """
    Extract (username, password) from an Authorization header.
    Returns (None, None) if invalid.
    Expected: 'Basic base64(username:password)'
    """
    if not auth_header or not auth_header.startswith("Basic "):
        return None, None

    encoded = auth_header.split(" ", 1)[1].strip()
    try:
        decoded = base64.b64decode(encoded).decode("utf-8")
    except Exception:
        return None, None

    if ":" not in decoded:
        return None, None

    username, password = decoded.split(":", 1)
    return username, password


def is_authorized(headers, valid_username: str = "admin", valid_password: str = "password123") -> bool:
    """
    Check Basic Auth credentials from request headers.
    headers is typically BaseHTTPRequestHandler.headers
    """
    auth_header = headers.get("Authorization")
    username, password = _parse_basic_header(auth_header)
    return username == valid_username and password == valid_password


def send_unauthorized(handler, realm: str = DEFAULT_REALM) -> None:
    """
    Send a 401 Unauthorized response using a BaseHTTPRequestHandler instance.
    """
    handler.send_response(401)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("WWW-Authenticate", f'Basic realm="{realm}"')
    handler.end_headers()

    payload = {
        "status": "error",
        "message": "Unauthorized. Provide valid Basic Authentication credentials.",
        "error_code": "UNAUTHORIZED",
    }
    handler.wfile.write(json.dumps(payload).encode("utf-8"))
