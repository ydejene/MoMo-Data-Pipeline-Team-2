"""
MoMo Transaction REST API Server
Provides CRUD endpoints for managing MoMo transaction data with Basic Authentication.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class TransactionAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Transaction API with CRUD operations."""
    
    # Class-level storage for transactions
    transactions_list = []
    transactions_dict = {}
    next_id = 1

    def do_GET(self):
        """Handle GET requests."""
        # Check authentication
        if not self.check_authentication():
            self.send_unauthorized()
            return
        
        # Parse URL
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        # Route: GET /transactions
        if path_parts[0] == 'transactions' and len(path_parts) == 1:
            self.get_all_transactions()
        
        # Route: GET /transactions/{id}
        elif path_parts[0] == 'transactions' and len(path_parts) == 2:
            try:
                transaction_id = int(path_parts[1])
                self.get_transaction_by_id(transaction_id)
            except ValueError:
                self.send_json_response(400, {
                    'status': 'error',
                    'message': 'Invalid transaction ID',
                    'error_code': 'INVALID_ID'
                })
        
        else:
            self.send_json_response(404, {
                'status': 'error',
                'message': 'Endpoint not found',
                'error_code': 'NOT_FOUND'
            })


        # ========== CRUD Operations ==========
    
    def get_all_transactions(self):
        """GET /transactions - List all transactions."""
        response = {
            'status': 'success',
            'message': 'Transactions retrieved successfully',
            'data': {
                'total_count': len(self.transactions_list),
                'transactions': self.transactions_list
            }
        }
        self.send_json_response(200, response)
    
    def get_transaction_by_id(self, transaction_id):
        """GET /transactions/{id} - Get single transaction."""
        # Use dictionary for O(1) lookup
        transaction = self.transactions_dict.get(transaction_id)
        
        if transaction:
            response = {
                'status': 'success',
                'message': 'Transaction retrieved successfully',
                'data': transaction
            }
            self.send_json_response(200, response)
        else:
            response = {
                'status': 'error',
                'message': f'Transaction with ID {transaction_id} not found',
                'error_code': 'TRANSACTION_NOT_FOUND'
            }
            self.send_json_response(404, response)


    