import socket
import threading

clients = {}
PASSWORD = "udpudp"  # Password for the chatroom

def handle_client(server_socket):
    while True:
        try:
            message, client_address = server_socket.recvfrom(1024)
            decoded_message = message.decode()

            # Proses login
            if decoded_message.startswith("LOGIN:"):
                _, username, password = decoded_message.split(":")
                
                # Verifikasi password
                if password != PASSWORD:
                    server_socket.sendto("Invalid password.".encode(), client_address)
                    continue
                
                # Cek apakah username sudah ada
                if username in clients.values():
                    server_socket.sendto("Username already taken.".encode(), client_address)
                    continue

                # Tambahkan klien baru
                clients[client_address] = username
                print(f"User {username} has joined the chat.")
                server_socket.sendto("Login successful!".encode(), client_address)
                continue

            # Ambil username pengirim berdasarkan alamat klien
            if client_address in clients:
                username = clients[client_address]
                print(f"{username}: {decoded_message}")

                # Siarkan pesan ke semua klien dengan format "username: pesan"
                for client in clients:
                    if client != client_address:  # Menghindari mengirim pesan kembali ke pengirim
                        server_socket.sendto(f"{username}: {decoded_message}".encode(), client)
            else:
                server_socket.sendto("Please log in first.".encode(), client_address)

        except Exception as e:
            print(f"Error: {e}")
            continue

def main():
    # Buat socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 12345))  # Bind ke semua interface dan port 12345
    print("Server is running and waiting for clients...")

    server_thread = threading.Thread(target=handle_client, args=(server_socket,))
    server_thread.daemon = True
    server_thread.start()

    server_thread.join()

if __name__ == "__main__":
    main()