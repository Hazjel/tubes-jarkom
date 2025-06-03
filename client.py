import socket
import sys
import time

def start_client(ip, port, file):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.connect((ip, port))

    request = f"GET /{file} HTTP/1.1\r\nHost: {ip}:{port}\r\n\r\n"
    
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    print(response)
    
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(data.decode(), end='')

    # Sleep for 10 seconds before closing
    time.sleep(10)
    client_socket.close()
    
if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    file = sys.argv[3]
    
    start_client(ip, port, file)