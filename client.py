import argparse
import socket

# Set the default host and port
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 3000


# Parse command line arguments
parser = argparse.ArgumentParser(description='HTTP Client')
parser.add_argument('host', metavar='host', type=str, nargs='?', default=DEFAULT_HOST,
                    help='Server IP address or host name')
parser.add_argument('port', metavar='port', type=int, nargs='?', default=DEFAULT_PORT,
                    help='Server port number')
parser.add_argument('path', metavar='path', type=str,
                    help='Path of the requested object on the server')
args = parser.parse_args()

# Send the HTTP GET request and display the server's response
# Open a TCP connection to the server

host = args.host
port = args.port
path = "/" + args.path

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((host, port))

    # Send the HTTP GET request to the server
    request = f'GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n'
    client_socket.sendall(request.encode())

    # Receive the server's response
    response = b''
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data
    print(response.decode())
