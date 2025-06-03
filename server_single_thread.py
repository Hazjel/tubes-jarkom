import socket
import sys
import time

def handle_client(connection_socket):
    try:
        print(f"Mulai memproses request dari client...")
        msg = connection_socket.recv(1024).decode()
        fname = msg.split()[1]
        f = open(fname[1:], encoding=('utf-8'))
        out = f.read()

        # Tambahkan delay untuk simulasi proses yang memakan waktu
        time.sleep(5)  # Delay 5 detik untuk demonstrasi
        print("Mengirim response ke client...")

        connection_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        for i in range(0, len(out)):
            connection_socket.send(out[i].encode())
        connection_socket.send("\r\n".encode())   
        
        # Tunggu konfirmasi dari client sebelum menutup koneksi
        while True:
            try:
                client_response = connection_socket.recv(1024).decode()
                if "Y" in client_response.upper():
                    print("Client meminta untuk mengakhiri koneksi")
                    break
            except:
                break

        connection_socket.close()
        print("Selesai memproses request dari client\n")

    except IOError:
        connection_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connection_socket.send("<html> <head> </head> <body> <h1> 404 Not Found </h1> </body> </html> \r\n".encode())
        connection_socket.close() 


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 5465))
server_socket.listen(1)  # Ubah ke 1 untuk membatasi antrian

print("Server single thread siap melayani...")
print("Server ini akan memproses satu client pada satu waktu.")
print("Setiap request akan diproses selama 5 detik untuk demonstrasi.\n")

try:
    while True:
        print("Menunggu koneksi client baru...")
        connection_socket, addr = server_socket.accept()
        print(f"Terkoneksi dengan {addr}")
        handle_client(connection_socket)  # Handle client directly without threading

except KeyboardInterrupt:
    print("\nShutting down server...")
    server_socket.close()
    sys.exit() 