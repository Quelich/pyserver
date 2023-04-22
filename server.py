import socket
import sys
import threading

MESSAGE = {
    "SUCCESS": "HTTP/1.1 200 OK\r\n\r\n",
    "NOT_FOUND": "HTTP/1.1 404 Not Found\r\n\r\n",
}


def start_server(host, port):
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Prepare socket
    server_socket.bind((host, port))
    server_socket.listen()

    while True:
        # Establish the connection
        connection_socket, addr = server_socket.accept()

        try:
            # Receive HTTP request
            message = connection_socket.recv(4096).decode()

            # Handle HTTP request
            filename = message.split()[1]  # parse
            with open(filename[1:]) as file:
                # Return a 200 OK response with the file's contents
                output_data = file.read()

            # Generate response
            response = MESSAGE["SUCCESS"] + output_data

            # Send response to client
            connection_socket.sendall(response.encode())

        except FileNotFoundError:
            # Send response message for file not found
            response = MESSAGE["NOT_FOUND"]
            response += "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
            connection_socket.sendall(response.encode())

        finally:
            # Close the connection socket
            connection_socket.close()


def end_server(server_socket):
    # Close the server socket
    server_socket.close()
    sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == '__main__':
    # Define host and port
    host = 'localhost'
    port = 3000

    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server, args=(host, port))
    server_thread.start()

    # Wait for user to press space bar
    input("Press space to stop the server\n")

    # End server
    end_server(server_socket)
