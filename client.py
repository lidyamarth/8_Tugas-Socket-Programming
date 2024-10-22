import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            print(message.decode())
        except Exception as e:
            print(f"Error: {e}")
            break

def main():
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    username = input("Enter your username: ")
    password = input("Enter the chatroom password: ")

    # Buat socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Kirim login informasi ke server
    login_message = f"LOGIN:{username}:{password}"
    client_socket.sendto(login_message.encode(), (server_ip, server_port))

    # Buat thread untuk menerima pesan dari server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    # Loop untuk mengirimkan pesan ke server
    while True:
        try:
            message = input()
            if message.lower() == 'exit':
                print("Exiting chat...")
                break
            client_socket.sendto(message.encode(), (server_ip, server_port))
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()