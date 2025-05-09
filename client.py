import socket
import sys

def start_client(ip, port, file):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.connect((ip, port))

