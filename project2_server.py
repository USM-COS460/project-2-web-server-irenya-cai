import socket
from threading import Thread
from datetime import datetime
import os
import mimetypes
import argparse

# Client Handler Thread: handles each client connection per thread
class ClientHandler(Thread):
    def __init__(self, client, address, document_root):
        Thread.__init__(self)
        self.client = client # the connected client socket
        self.address = address # the client address
        self.document_root = document_root # the root directory to serve files from

    # Thread run method to handle client requests 
    def run(self):
        print(f"Client connected from {self.address}")

        try:
            # Get up to 1024 bytes from the client and decode to string
            request = self.client.recv(1024).decode('utf-8') 
            
            if not request:
                return # if no data received, exit
            
            # Get the first line of the request, ex. GET /index.html HTTP/1.1
            request_line = request.splitlines()[0] 
            # print(f"Request: {request_line}")
            
            # Split the request line into method (GET), path (index.html), and HTTP version (HTTP/1.1)
            method, path, version = request_line.split()

            # If the method is not GET, repond with 405 Method Not Allowed
            if method != 'GET':
                self.send_response(405, b"<h1>405 Method Not Allowed</h1>")
                return
            
            # File Path Mapping, map '/' to '/index.html'
            if path == '/':
                path = '/index.html'

            # The full file path on the server from the document root and requested path
            filepath = os.path.join(self.document_root, path.strip('/'))

            # Check if file exists and is a file
            if os.path.exists(filepath) and os.path.isfile(filepath):
                with open(filepath, 'rb') as f: # Open the file in binary mode by reading as bytes, rb = read bytes
                    body = f.read() # Read the file content
                self.send_response(200, body, filepath) # If the file exists, read its contents in binary and send a 200 OK response
            else:
                self.send_response(404, b"<h1>404 Not Found</h1>") # If the file does not exist, send a 404 Not Found response
        
        # Catch any other exceptions and send 500 Internal Error
        except Exception as e:
            print("Error:", e)
            self.send_response(500, b"<h1>500 Internal Error</h1>") 
        finally:
            self.client.close() # Close the client connection

    # Method to send HTTP response to the client
    def send_response(self, status_code, body, filepath=None):
        if status_code == 200:
            status_message = "HTTP/1.1 200 OK\r\n"
        elif status_code == 404:
            status_message = "HTTP/1.1 404 Not Found\r\n"
        elif status_code == 405:
            status_message = "HTTP/1.1 405 Method Not Allowed\r\n"
        else:
            status_message = "HTTP/1.1 500 Internal Error\r\n"
        
        # Determine content type based on file extension
        content_type = mimetypes.guess_type(filepath or "")[0]

        
        current_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        # HTTP reponse headers
        headers = (
            f"Date: {current_date}\r\n"
            "Server: BobsDiscountServer/1.0\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
        )

        # Combine status line and headers, then send the headers and the body
        response = status_message + headers 
        self.client.sendall(response.encode('utf-8') + body)

# Main server loop to start the HTTP server, listen for client connections, and accept them
def main():
    # Parse command line arguments for port and document root
    parser = argparse.ArgumentParser(description="Simple HTTP Server")
    parser.add_argument("--port", type=int, default=1010, help="Port number to listen on")
    parser.add_argument("--root", type=str, default="./www", help="Document root directory")
    args = parser.parse_args()

    host = "localhost"
    port = args.port
    document_root = args.root

    # The server socket setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create TCP socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow address reuse
    server_socket.bind((host, port)) # bind to host and port
    server_socket.listen() # listen for incoming connections
    print(f"Server listening on {host}:{port}") 
    print(f"Serving files from: {document_root}")

    # Server loop to accept client connections
    while True:
        client, address = server_socket.accept()
        client_thread = ClientHandler(client, address, document_root) #create a new thread for each client
        client_thread.start()

if __name__ == "__main__":
    main()
