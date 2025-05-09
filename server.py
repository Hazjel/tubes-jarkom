import socket
import threading

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 80

    server_socket.bind((host, port))

    server_socket.listen(5)

    print(f"Server terhubung di alamat {host} dan port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Terhubung dengan {addr}")

        data = client_socket.recv(1024).decode('utf-8')
        