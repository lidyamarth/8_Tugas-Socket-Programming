import socket
import threading

clients = {}
PASSWORD = "udpudp"  # Password untuk ruangan chat

def handle_client(server_socket):
    while True:
        try:
            message, client_address = server_socket.recvfrom(1024)
            decoded_message = message.decode()

            # Proses login
            if decoded_message.startswith("LOGIN:"):
                _, username, password = decoded_message.split(":")

                # Verifikasi password dalam loop
                while password != PASSWORD:
                    # Jika password salah, kirim pesan untuk input ulang
                    server_socket.sendto("Invalid password. Please try again.".encode(), client_address)
                    message, client_address = server_socket.recvfrom(1024)
                    decoded_message = message.decode()

                    # Update username dan password dari pesan ulang
                    if decoded_message.startswith("LOGIN:"):
                        _, username, password = decoded_message.split(":")

                # Cek apakah ruangan sudah penuh
                if len(clients) >= 2:
                    server_socket.sendto("Chat room is full.".encode(), client_address)
                    continue

                # Cek apakah username sudah ada
                if username in clients.values():
                    server_socket.sendto("Username already taken.".encode(), client_address)
                    continue

                # Tambahkan klien baru
                clients[client_address] = username
                print(f"User {username} has joined the chat.")
                server_socket.sendto("Login successful! You are connected.".encode(), client_address)

                # Beritahu klien lain jika ada yang masuk
                for addr in clients:
                    if addr != client_address:
                        server_socket.sendto(f"{username} has joined the chat.".encode(), addr)
                continue

            # Proses pesan one-to-one antara dua klien yang terhubung
            if client_address in clients:
                username = clients[client_address]

                # Deteksi jika klien keluar
                if decoded_message.lower() == 'exit':
                    print(f"User {username} has left the chat.")
                    del clients[client_address]
                    server_socket.sendto("You have left the chat.".encode(), client_address)

                    # Beritahu klien lain bahwa pasangan obrolan keluar
                    for addr in clients:
                        server_socket.sendto(f"{username} has left the chat.".encode(), addr)
                    continue

                # Kirimkan pesan ke klien lain jika ada dua klien terhubung
                other_clients = [addr for addr in clients if addr != client_address]
                if other_clients:
                    other_client = other_clients[0]
                    formatted_message = f"{username}: {decoded_message}"
                    server_socket.sendto(formatted_message.encode(), other_client)
                else:
                    server_socket.sendto("No other user is connected.".encode(), client_address)

        except Exception as e:
            print(f"Error: {e}")
            # Jika terjadi error, hapus klien dari daftar
            if client_address in clients:
                username = clients[client_address]
                del clients[client_address]
                print(f"User {username} has been removed due to an error.")

                # Beritahu klien lain bahwa pasangan obrolan keluar
                for addr in clients:
                    server_socket.sendto(f"{username} has left the chat.".encode(), addr)
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
