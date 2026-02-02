# api/auth.py
import base64
import json
import sys
from pathlib import Path

DEFAULT_REALM = "MoMo SMS API"

# Allow importing database modules when running api/app.py directly
sys.path.append(str(Path(__file__).parent.parent / "database"))

from db_config import get_session
from models import User


def _parse_basic_header(auth_header: str):
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


def is_authorized(headers) -> bool:
    """
    Validate Basic Auth credentials against the User table in SQLite.
    headers is typically BaseHTTPRequestHandler.headers
    """
    auth_header = headers.get("Authorization")
    username, password = _parse_basic_header(auth_header)

    if not username or not password:
        return False

    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return False

        # NOTE: this project stores plain text password (password_text)
        # In real systems you'd store a hashed password and verify with bcrypt/argon2.
        return user.password_text == password
    finally:
        session.close()


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
