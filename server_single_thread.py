import socket
import sys
import time

def handle_client(connection_socket, client_address):
    try:
        print(f"\n[+] Mulai memproses request dari client {client_address}")
        msg = connection_socket.recv(1024).decode()
        fname = msg.split()[1]
        f = open(fname[1:], encoding=('utf-8'))
        out = f.read()

        # Tambahkan delay untuk simulasi proses yang memakan waktu
        time.sleep(5)  # Delay 5 detik untuk demonstrasi
        print(f"[*] Mengirim response ke client {client_address}...")

        connection_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        for i in range(0, len(out)):
            connection_socket.send(out[i].encode())
        connection_socket.send("\r\n".encode())   
        
        # Tunggu konfirmasi dari client sebelum menutup koneksi
        while True:
            try:
                client_response = connection_socket.recv(1024).decode()
                if "Y" in client_response.upper():
                    print(f"[*] Client {client_address} meminta untuk mengakhiri koneksi")
                    break
            except:
                break

        connection_socket.close()
        print(f"[-] Koneksi dengan client {client_address} telah terputus")
        print(f"[+] Server siap menerima koneksi baru\n")
        print("="*50)

    except IOError:
        connection_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connection_socket.send("<html> <head> </head> <body> <h1> 404 Not Found </h1> </body> </html> \r\n".encode())
        connection_socket.close()
        print(f"[-] Koneksi dengan client {client_address} terputus karena file tidak ditemukan")
        print(f"[+] Server siap menerima koneksi baru\n")
        print("="*50)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 5465))
server_socket.listen(1)  # Ubah ke 1 untuk membatasi antrian

print("="*50)
print("[+] Server single thread siap melayani...")
print("[*] Server ini akan memproses satu client pada satu waktu.")
print("[*] Setiap request akan diproses selama 5 detik untuk demonstrasi.")
print("[+] Menunggu koneksi client...\n")

try:
    while True:
        connection_socket, addr = server_socket.accept()
        print(f"[+] Menerima koneksi baru dari {addr}")
        handle_client(connection_socket, addr)  # Pass the client address

except KeyboardInterrupt:
    print("\n[-] Shutting down server...")
    server_socket.close()
    sys.exit()
except Exception as e:
    print(f"\n[-] Terjadi error: {e}")
    server_socket.close()
    sys.exit() 