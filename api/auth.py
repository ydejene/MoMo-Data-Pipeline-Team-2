"""
Authentication utilities for MoMo SMS API

This module provides helper functions for Basic Authentication.
Note: The actual authentication is implemented inline in app.py
This file exists for documentation and code organization purposes.
"""

import base64
import sys
from pathlib import Path

# Add database to path
sys.path.append(str(Path(__file__).parent.parent / 'database'))

from db_config import get_session
from models import User


def verify_credentials(username, password):
    """
    Verify username and password against database
    
    Args:
        username (str): Username to verify
        password (str): Plain text password to verify
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and user.password_text == password:
            return True
        return False
    except Exception as e:
        print(f"Database error during authentication: {e}")
        return False
    finally:
        session.close()


def decode_basic_auth(auth_header):
    """
    Decode Basic Authentication header
    
    Args:
        auth_header (str): Authorization header value (e.g., "Basic YWRtaW46cGFzc3dvcmQ=")
        
    Returns:
        tuple: (username, password) if valid, (None, None) if invalid
    """
    if not auth_header or not auth_header.startswith('Basic '):
        return None, None
    
    try:
        # Extract and decode Base64 credentials
        encoded = auth_header.split(' ')[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        username, password = decoded.split(':', 1)
        return username, password
    except Exception as e:
        print(f"Error decoding auth header: {e}")
        return None, None


def authenticate_request(headers):
    """
    Complete authentication flow for HTTP request
    
    Args:
        headers: HTTP request headers object
        
    Returns:
        bool: True if authenticated, False otherwise
        
    Example:
        if authenticate_request(self.headers):
            # Process request
        else:
            # Return 401 Unauthorized
    """
    auth_header = headers.get('Authorization')
    username, password = decode_basic_auth(auth_header)
    
    if not username or not password:
        return False
    
    return verify_credentials(username, password)