import socket
import threading

def receive_messages(client_socket):
    global authenticated  # Tambahkan variabel global untuk status otentikasi
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            decoded_message = message.decode()
            print(decoded_message)
            
            # Jika password salah dan belum otentikasi, minta input ulang
            if "Invalid password" in decoded_message and not authenticated:
                password = input("Please re-enter the password: ")
                login_message = f"LOGIN:{username}:{password}"
                client_socket.sendto(login_message.encode(), (server_ip, server_port))

            # Jika login berhasil, ubah status otentikasi
            elif "Login successful" in decoded_message:
                authenticated = True

        except Exception as e:
            print(f"Error: {e}")
            break

def main():
    global username, server_ip, server_port, authenticated  # Tambahkan variabel authenticated
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    username = input("Enter your username: ")
    password = input("Enter the chatroom password: ")

    authenticated = False  # Set status otentikasi ke False saat memulai

    # Buat socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Kirim login informasi ke server
    login_message = f"LOGIN:{username}:{password}"
    client_socket.sendto(login_message.encode(), (server_ip, server_port))

    # Buat thread untuk menerima pesan dari server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    # Tunggu hingga otentikasi berhasil sebelum memasuki loop pengiriman pesan
    while not authenticated:
        pass

    # Loop untuk mengirimkan pesan ke server setelah otentikasi berhasil
    while True:
        try:
            message = input("Enter message (or type 'exit' to leave): ")
            if message.lower() == 'exit':
                client_socket.sendto(message.encode(), (server_ip, server_port))
                print("Exiting chat...")
                break
            client_socket.sendto(message.encode(), (server_ip, server_port))
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()