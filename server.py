import socket
import threading

clients = {}

def handle_client(server_socket):
    while True:
        try:
            message, client_address = server_socket.recvfrom(1024)
            decoded_message = message.decode()

            # Menyimpan username
            if decoded_message.startswith("LOGIN:"):
                username = decoded_message.split(":")[1]
                clients[client_address] = username
                print(f"User {username} has joined the chat.")
                continue

            # Ambil username pengirim berdasarkan alamat klien
            username = clients[client_address]  # Mengambil username dari dictionary clients
            print(f"{username}: {decoded_message}")  # Menampilkan pesan di server

            # Tampilkan pesan ke semua klien dengan format "username: pesan"
            for client in clients:
    #            if client != client_address:  # Kirim pesan kembali ke pengirim???
                server_socket.sendto(f"{username}: {decoded_message}".encode(), client)

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
