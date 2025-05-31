import socket
import threading
import sys
from concurrent.futures import ThreadPoolExecutor

def handle_client(connection_socket):
    try:
        msg = connection_socket.recv(1024).decode()
        fname = msg.split()[1]
        f = open(fname[1:], encoding=('utf-8'))
        out = f.read()

        connection_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        for i in range(0, len(out)):
            connection_socket.send(out[i].encode())
        connection_socket.send("\r\n".encode())   

    except IOError:
        connection_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connection_socket.send("<html> <head> </head> <body> <h1> 404 Not Found </h1> </body> </html> \r\n".encode())
    finally:
        connection_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 5465))
    server_socket.listen(5)

    print("Server multi thread siap melayani...")

    # Create a thread pool with maximum 10 threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        try:
            while True:
                connection_socket, addr = server_socket.accept()
                print(f"Terkoneksi dengan {addr}")
                executor.submit(handle_client, connection_socket)

        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            server_socket.close()

if __name__ == "__main__":
    main()
    sys.exit() 