import socket

def send_message(message: str, server_address: str, server_port: int) -> str:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_address, server_port))
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        return response
    finally:
        client_socket.close()

# Assuming the server is running on localhost and port 12345
server_address = "localhost"
server_port = 12345


def start():
    send_message("main","localhost",12345)

    

start()