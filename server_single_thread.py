import socket
import sys

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 5465))
server_socket.listen(1)

print("Server siap melayani...")

while True:
    connection_socket, addr = server_socket.accept()
    print(f"Terkoneksi dengan {addr}")
    
    try:
        msg = connection_socket.recv(1024).decode()
        fname = msg.split()[1]
        f = open(fname[1:], encoding=('utf-8'))
        out = f.read()

        connection_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        for i in range(0, len(out)):
            connection_socket.send(out[i].encode())
        connection_socket.send("\r\n".encode())   

        connection_socket.close()

    except IOError:
        connection_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connection_socket.send("<html> <head> </head> <body> <h1> 404 Not Found </h1> </body> </html> \r\n".encode())
        connection_socket.close()

server_socket.close()
sys.exit()