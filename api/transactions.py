from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re

demoResponse = "Success!"
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
    
    # Test
    def do_GET(self):
        if(self.path == '/'):
            # debugging
            self._set_headers(200)
            # we first serilize (dict -> json string then encode('utf-8') because HTTP wfile.write expects bytes and JSON strings is the one with the encode() method )
            self.wfile.write(json.dumps({"demoResponse":"Success"}).encode())
            #  If you already have a JSON string literal you may encode it directly, but using json.dumps avoids mistakes and ensures correct escaping/encoding.
            # self.wfile.write('{"demoResponse":"Success"}'.encode())
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


# Run the server
def run (port=8000):
    '''
    This function starts the http server on port 8000(common port for development.)
    '''
    # Creating the server (TransactionHandler tells the server how to handle requests)
    server = HTTPServer(("localhost", port),TransactionHandler)

    # print a message for debugging 
    print(f"Server running at http://localhost:{port}")

    # Keeping the server run until it's is stopped
    server.serve_forever()

# Only calls run() when the file directly is run but is not importes
if __name__ == "__main__":
    run()