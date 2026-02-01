from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re

# HTTP request (transactions) handler: subclassing from BaseHTTPRequestHandler 
class TransactionHandler(BaseHTTPRequestHandler):
    '''
    Handles client request (API calls either from browser, postman, curl) and decides what to respond back.
    '''
    # Helper Method to set the headers (meta data handler)
    def _set_headers(self, status = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'Application/json')
        self.end_headers()
    
    # Handling PUT(UPDATE) requests
    def do_PUT(self):
        '''
        respondes/handles PUT(UPDATE) requests of client on the end point /transactions/{id}
        self.path gives access the api end point a user is making request
        '''
        # using regex to extract the id's from the end point
        pattern = r'^/transactions/(\d+)'
        result = re.match(pattern, self.path)
        if not result:
            return self._set_headers(400)
        else:
            extracted_id = int(result.group(1))



