from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import base64
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Add database to path
sys.path.append(str(Path(__file__).parent.parent / 'database'))

from db_config import get_session
from models import Transaction, User, TransactionCategory, TransactionFee, FeeType, SystemLog
from datetime import datetime

class TransactionHandler(BaseHTTPRequestHandler):
    
    def _set_headers(self, status=200):
        """Set response headers"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def _authenticate(self):
        """Verify Basic Authentication"""
        auth_header = self.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Basic '):
            return False
        
        try:
            # Decode Base64 credentials
            encoded = auth_header.split(' ')[1]
            decoded = base64.b64decode(encoded).decode('utf-8')
            username, password = decoded.split(':', 1)
            
            # Query database for user
            session = get_session()
            try:
                user = session.query(User).filter_by(username=username).first()
                if user and user.password_text == password:
                    return True
            finally:
                session.close()
            
            return False
            
        except Exception as e:
            print(f"Auth error: {e}")
            return False
    
    def _send_unauthorized(self):
        """Send 401 Unauthorized response"""
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="MoMo SMS API"')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'error': 'Unauthorized',
            'message': 'Valid credentials required'
        }).encode())
    
    def _transaction_to_dict(self, transaction):
        """Convert SQLAlchemy Transaction model to dictionary"""
        return {
            'transaction_id': transaction.transaction_id,
            'external_ref': transaction.external_ref,
            'amount': float(transaction.amount),
            'currency': transaction.currency,
            'transaction_status': transaction.transaction_status,
            'sender_notes': transaction.sender_notes,
            'transaction_date': transaction.transaction_date.isoformat() if transaction.transaction_date else None,
            'counter_party': transaction.counter_party,
            'created_at': transaction.created_at.isoformat() if transaction.created_at else None,
            'category': {
                'category_id': transaction.category.category_id,
                'category_name': transaction.category.category_name,
                'category_code': transaction.category.category_code
            } if transaction.category else None,
            'user': {
                'user_id': transaction.user.user_id,
                'full_name': transaction.user.full_name,
                'phone_number': transaction.user.phone_number
            } if transaction.user else None,
            'fees': [
                {
                    'fee_type': fee.fee_type.fee_name,
                    'amount': float(fee.transaction_fee_amount)
                } for fee in transaction.fees
            ] if transaction.fees else []
        }
    
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self._set_headers(200)
    
    def do_GET(self):
        """Handle GET requests"""
        # Check authentication
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        session = get_session()
        
        try:
            # GET /transactions - List all transactions
            if self.path == '/transactions' or self.path.startswith('/transactions?'):
                # Parse query parameters
                parsed_url = urlparse(self.path)
                query_params = parse_qs(parsed_url.query)
                
                # Build query
                query = session.query(Transaction)
                
                # Apply filters
                if 'status' in query_params:
                    status = query_params['status'][0]
                    query = query.filter(Transaction.transaction_status == status)
                
                if 'category' in query_params:
                    category_code = query_params['category'][0]
                    query = query.join(TransactionCategory).filter(
                        TransactionCategory.category_code == category_code
                    )
                
                # Execute query
                transactions = query.all()
                
                result = {
                    'success': True,
                    'count': len(transactions),
                    'data': [self._transaction_to_dict(t) for t in transactions]
                }
                
                self._set_headers(200)
                self.wfile.write(json.dumps(result, indent=2).encode())
            
            # GET /transactions/{id} - Get single transaction
            elif re.match(r'^/transactions/\d+$', self.path):
                transaction_id = int(self.path.split('/')[-1])
                transaction = session.query(Transaction).get(transaction_id)
                
                if not transaction:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({
                        'error': 'Not Found',
                        'message': f'Transaction {transaction_id} not found'
                    }).encode())
                    return
                
                result = {
                    'success': True,
                    'data': self._transaction_to_dict(transaction)
                }
                
                self._set_headers(200)
                self.wfile.write(json.dumps(result, indent=2).encode())
            
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({
                    'error': 'Not Found',
                    'message': 'Endpoint not found'
                }).encode())
        
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            }).encode())
        
        finally:
            session.close()
    
    def do_POST(self):
        """Handle POST requests - Create new transaction"""
        # Check authentication
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        session = get_session()
        
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    'error': 'Bad Request',
                    'message': 'Request body required'
                }).encode())
                return
            
            raw_body = self.rfile.read(content_length)
            data = json.loads(raw_body.decode('utf-8'))
            
            # Validate required fields
            required_fields = ['external_ref', 'amount', 'raw_data', 'transaction_date']
            missing_fields = [f for f in required_fields if f not in data]
            if missing_fields:
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    'error': 'Bad Request',
                    'message': f'Missing required fields: {", ".join(missing_fields)}'
                }).encode())
                return
            
            # Get default user
            default_user = session.query(User).first()
            
            # Get category (default to TRANSFER if not specified)
            category_code = data.get('category_code', 'TRANSFER')
            category = session.query(TransactionCategory).filter_by(
                category_code=category_code
            ).first()
            
            if not category:
                category = session.query(TransactionCategory).filter_by(
                    category_code='TRANSFER'
                ).first()
            
            # Parse transaction date
            trans_date = datetime.fromisoformat(data['transaction_date'])
            
            # Create transaction
            transaction = Transaction(
                external_ref=data['external_ref'],
                amount=data['amount'],
                currency=data.get('currency', 'RWF'),
                transaction_status=data.get('transaction_status', 'COMPLETED'),
                sender_notes=data.get('sender_notes'),
                raw_data=data['raw_data'],
                transaction_date=trans_date,
                counter_party=data.get('counter_party'),
                created_at=datetime.now(),
                category_id=category.category_id,
                user_id=default_user.user_id
            )
            
            session.add(transaction)
            session.flush()
            
            # Add fee if specified
            if 'fee_amount' in data:
                fee_type = session.query(FeeType).filter_by(
                    fee_name='Transaction Fee'
                ).first()
                
                if fee_type:
                    fee = TransactionFee(
                        transaction_fee_amount=data['fee_amount'],
                        created_at=datetime.now(),
                        transaction_id=transaction.transaction_id,
                        fee_type_id=fee_type.fee_type_id
                    )
                    session.add(fee)
            
            session.commit()
            
            result = {
                'success': True,
                'message': 'Transaction created successfully',
                'data': self._transaction_to_dict(transaction)
            }
            self._set_headers(201)
            self.wfile.write(json.dumps(result, indent=2).encode())

        except json.JSONDecodeError:    
            self._set_headers(400)
            self.wfile.write(json.dumps({
                'error': 'Bad Request',
                'message': 'Invalid JSON in request body'
            }).encode())
    
        except Exception as e:
            session.rollback()
            self._set_headers(500)
            self.wfile.write(json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            }).encode())
        
        finally:
            session.close()

    def do_PUT(self):
        """Handle PUT requests - Update transaction"""
        # Check authentication
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        # Extract transaction ID from URL
        pattern = r'^/transactions/(\d+)$'
        match = re.match(pattern, self.path)
        
        if not match:
            self._set_headers(400)
            self.wfile.write(json.dumps({
                'error': 'Bad Request',
                'message': 'Invalid endpoint format. Use /transactions/{id}'
            }).encode())
            return
        
        transaction_id = int(match.group(1))
        session = get_session()
        
        try:
            # Find transaction
            transaction = session.query(Transaction).get(transaction_id)
            
            if not transaction:
                self._set_headers(404)
                self.wfile.write(json.dumps({
                    'error': 'Not Found',
                    'message': f'Transaction {transaction_id} not found' 
            
                }).encode())
                return
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    'error': 'Bad Request',
                    'message': 'Request body required'
                }).encode())
                return
            
            raw_body = self.rfile.read(content_length)
            update_data = json.loads(raw_body.decode('utf-8'))
            
            # Update allowed fields only
            allowed_fields = [
                'amount', 'transaction_status', 'sender_notes', 
                'counter_party', 'currency'
            ]
            
            for key, value in update_data.items():
                if key in allowed_fields:
                    setattr(transaction, key, value)
            
            session.commit()
            
            result = {
                'success': True,
                'message': 'Transaction updated successfully',
                'data': self._transaction_to_dict(transaction)
            }
            
            self._set_headers(200)
            self.wfile.write(json.dumps(result, indent=2).encode())
        
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({
                'error': 'Bad Request',
                'message': 'Invalid JSON in request body'
            }).encode())
        
        except Exception as e:
            session.rollback()
            self._set_headers(500)
            self.wfile.write(json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            }).encode())
        
        finally:
            session.close()

    def do_DELETE(self):
        """Handle DELETE requests - Delete transaction"""
        # Check authentication
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        # Extract transaction ID from URL
        pattern = r'^/transactions/(\d+)$'
        match = re.match(pattern, self.path)
        
        if not match:
            self._set_headers(400)
            self.wfile.write(json.dumps({
                'error': 'Bad Request',
                'message': 'Invalid endpoint format. Use /transactions/{id}'
            }).encode())
            return
        
        transaction_id = int(match.group(1))
        session = get_session()
        
        try:
            # Find transaction
            transaction = session.query(Transaction).get(transaction_id)
            
            if not transaction:
                self._set_headers(404)
                self.wfile.write(json.dumps({
                    'error': 'Not Found',
                    'message': f'Transaction {transaction_id} not found'
                }).encode())
                return
            
            # Delete transaction (fees cascade automatically)
            session.delete(transaction)
            session.commit()
            
            result = {
                'success': True,
                'message': f'Transaction {transaction_id} deleted successfully'
            }
            
            self._set_headers(200)
            self.wfile.write(json.dumps(result).encode())
        
        except Exception as e:
            session.rollback()
            self._set_headers(500)
            self.wfile.write(json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            }).encode())
        
        finally:
            session.close()


def run(port=8000):
    """Start the HTTP server"""
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, TransactionHandler)
    print(f"MoMo SMS API Server running at http://localhost:{port}")
    print(f"Username: admin")
    print(f"Password: password123")
    print(f"\n Press Ctrl+C to stop")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
        httpd.server_close()