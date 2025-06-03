import socket
import sys

def start_client(ip, port, file):
    while True:
        # Create new socket connection for each request
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
        
        # Close the current connection
        client_socket.close()
        
        # Ask user if they want to continue
        user_input = input("\nDo you want to make another request? (y/n): ")
        if user_input.lower() != 'y':
            break
    
if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    file = sys.argv[3]
    
    start_client(ip, port, file)