import socket
import threading
import tkinter as tk
from queue import Queue

def receive_messages(client_socket, message_queue, stop_event):
    global authenticated
    while not stop_event.is_set():  # Loop berjalan selama stop_event belum diatur
        try:
            message, _ = client_socket.recvfrom(1024)
            decoded_message = message.decode()
            message_queue.put((decoded_message, "server"))

            if "Invalid password" in decoded_message and not authenticated:
                message_queue.put(("Invalid password. Please re-enter the password.", "system"))
                password_entry.config(bg="red")
                login_frame.pack(padx=16, pady=8)
                chat_frame.pack_forget()

            elif "Username already taken" in decoded_message:
                message_queue.put(("Username already taken. Please choose another username.", "system"))
                username_entry.config(bg="red")
                login_frame.pack(padx=16, pady=8)

            elif "Login successful" in decoded_message:
                authenticated = True
                password_entry.config(bg="white")
                username_entry.config(bg="white")
                login_frame.pack_forget()
                chat_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
                entry_field.focus()
                message_queue.put(("You have entered the chat room.", "system"))

        except Exception as e:
            message_queue.put((f"Error: {e}", "system"))
            break

def display_message(message, sender):
    chat_display.config(state=tk.NORMAL)
    if sender == "user":
        chat_display.insert(tk.END, f"You: {message}\n", "user")
    elif sender == "server":
        chat_display.insert(tk.END, f"{message}\n", "server")
    else:
        chat_display.insert(tk.END, f"{message}\n", "system")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

def process_queue():
    while not message_queue.empty():
        message, sender = message_queue.get()
        display_message(message, sender)
    root.after(100, process_queue)

def send_message(event=None):
    global authenticated
    if authenticated:
        message = user_message.get()
        user_message.set("")
        display_message(message, "user")
        client_socket.sendto(message.encode(), (server_ip, server_port))
        if message.lower() == "exit":
            close_connection()

def close_connection():
    # Set stop event and close socket
    stop_event.set()  # Memberhentikan thread penerimaan pesan
    client_socket.close()  # Menutup soket
    root.quit()  # Keluar dari aplikasi Tkinter

def start_chat():
    global server_ip, server_port, username, password, client_socket, authenticated

    server_ip = ip_entry.get()
    server_port = int(port_entry.get())
    username = username_entry.get()
    password = password_entry.get()

    authenticated = False
    login_message = f"LOGIN:{username}:{password}"

    password_entry.config(bg="white")
    username_entry.config(bg="white")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(login_message.encode(), (server_ip, server_port))

    # Start the thread with stop_event
    threading.Thread(target=receive_messages, args=(client_socket, message_queue, stop_event)).start()

def on_login_button():
    # Run the chat starting process
    threading.Thread(target=start_chat).start()

def main():
    global root, login_frame, chat_frame, chat_display, user_message, message_queue, stop_event
    global ip_entry, port_entry, username_entry, password_entry, entry_field

    stop_event = threading.Event()  # Event untuk menghentikan thread penerimaan pesan

    root = tk.Tk()
    root.title("Chat Room")
    root.geometry("500x500")
    root.minsize(500, 500)

    root.protocol("WM_DELETE_WINDOW", close_connection)  # Menangani aksi keluar dari aplikasi

    # Login Frame
    login_frame = tk.Frame(root)
    login_frame.pack(padx=20, pady=8)

    heading_label = tk.Label(root, text="Welcome to Chat Room", font=("Satoshi Variable", 20, "bold"))
    heading_label.pack(pady=(80, 20))

    # Configure grid for login frame
    login_frame.grid_columnconfigure(0, weight=1)
    login_frame.grid_columnconfigure(1, weight=1)

    tk.Label(login_frame, text="Server IP:").grid(row=0, column=0, sticky="w")
    ip_entry = tk.Entry(login_frame)
    ip_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_frame, text="Server Port:").grid(row=1, column=0, sticky="w")
    port_entry = tk.Entry(login_frame)
    port_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(login_frame, text="Username:").grid(row=2, column=0, sticky="w")
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(login_frame, text="Password:").grid(row=3, column=0, sticky="w")
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=3, column=1, padx=5, pady=5)

    login_button = tk.Button(login_frame, text="Login", command=on_login_button)
    login_button.grid(row=4, columnspan=2, pady=10)

    # Center the login frame
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    chat_frame = tk.Frame(root)

    chat_display = tk.Text(chat_frame, wrap="word", state=tk.DISABLED, bg="#FEFEFE")
    chat_display.tag_config("user", foreground="blue")
    chat_display.tag_config("server", foreground="green")
    chat_display.tag_config("system", foreground="green")
    chat_display.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    user_message = tk.StringVar()
    entry_field = tk.Entry(chat_frame, textvariable=user_message)
    entry_field.bind("<Return>", send_message)
    entry_field.pack(pady=5, fill=tk.X, padx=5)

    send_button = tk.Button(chat_frame, text="Send", command=send_message)
    send_button.pack(pady=8)

    # Initialize the queue for communication between threads
    message_queue = Queue()

    root.after(100, process_queue)
    root.mainloop()

if __name__ == "__main__":
    main()