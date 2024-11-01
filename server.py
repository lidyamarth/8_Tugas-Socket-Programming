import socket
import threading
import tkinter as tk

# Konfigurasi server
SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345
BUFFER_SIZE = 1024
PASSWORD = "udpudp" 

# Inisialisasi UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

# Menyimpan informasi client
clients = {}

# Menampilkan message pada GUI
def display_chat_message(message):
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, message + "\n")
    chat_text.config(state=tk.DISABLED)
    chat_text.see(tk.END)

def display_log_message(message):
    chat_text.config(state=tk.NORMAL)
    centered_message = message.center(80)
    chat_text.insert(tk.END, centered_message + "\n")
    chat_text.config(state=tk.DISABLED)
    chat_text.see(tk.END)


def handle_client():
    display_log_message("Server is running and waiting for clients...")
    while True:
        try:
            message, client_address = server_socket.recvfrom(BUFFER_SIZE)
            decoded_message = message.decode()

            # login
            if decoded_message.startswith("LOGIN:"):
                _, username, password = decoded_message.split(":")
                
                # Cek password
                if password != PASSWORD:
                    server_socket.sendto("Invalid password. Please try again.".encode(), client_address)
                    continue

                # Cek availability chatroom
                if len(clients) >= 2:
                    server_socket.sendto("Chat room is full.".encode(), client_address)
                    continue

                # Cek unique username
                if username in clients.values():
                    server_socket.sendto("Username already taken.".encode(), client_address)
                    continue

                # Menambahkan client ke dalam daftar
                clients[client_address] = username
                display_log_message(f"User {username} has joined the chat.")
                server_socket.sendto("Login successful! You are connected.".encode(), client_address)

                # Informasi client lain yang memasuki chatroom
                for addr in clients:
                    if addr != client_address:
                        server_socket.sendto(f"{username} has joined the chat.".encode(), addr)
                continue

            # Pesan chatting
            if client_address in clients:
                username = clients[client_address]

                # Mendeteksi apabila ada client yang keluar
                if decoded_message.lower() == 'exit':
                    display_log_message(f"User {username} has left the chat.")
                    del clients[client_address]
                    server_socket.sendto("You have left the chat.".encode(), client_address)

                    # Menginformasikan client lain apabila client keluar
                    for addr in clients:
                        server_socket.sendto(f"{username} has left the chat.".encode(), addr)
                    continue

                # Mengirimkan pesan ke klien lain
                other_clients = [addr for addr in clients if addr != client_address]
                if other_clients:
                    other_client = other_clients[0]
                    formatted_message = f"{username}: {decoded_message}"
                    server_socket.sendto(formatted_message.encode(), other_client)
                    display_chat_message(formatted_message)
                else:
                    server_socket.sendto("No other user is connected.".encode(), client_address)

        except Exception as e:
            display_log_message(f"Error: {e}")
            if client_address in clients:
                username = clients[client_address]
                del clients[client_address]
                display_log_message(f"User {username} has been removed due to an error.")
                
                for addr in clients:
                    server_socket.sendto(f"{username} has left the chat.".encode(), addr)
            continue

# Konfigurasi GUI dengan Tkinter
root = tk.Tk()
root.title("UDP Server Chat Room")

# Widget Text untuk chat dan log
chat_text = tk.Text(root, width=80, height=20, wrap=tk.WORD)
chat_text.pack(padx=10, pady=10)
chat_text.config(state=tk.DISABLED)

# Menjalankan thread server
server_thread = threading.Thread(target=handle_client)
server_thread.daemon = True
server_thread.start()

# Menjalankan GUI
root.mainloop()
