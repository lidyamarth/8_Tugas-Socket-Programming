# II2120 - Jaringan Komputer
> Hands On UDP Socket Programming

# About
Aplikasi ini adalah chatroom sederhana berbasis UDP socket yang memungkinkan komunikasi antara beberapa client melalui server. Aplikasi ini menggunakan Python dan membutuhkan beberapa modul pendukung.

# Contributors
1. Desati Dinda Saraswati		  18223110
2. Lidya Marthadilla          18223134

# Specification
1. Server mampu menerima pesan yang dikirim client dan mencetaknya ke layar.
2. Server mampu meneruskan pesan satu client ke client lain.
3. Client mampu mengirimkan pesan ke server dengan IP dan port yang ditentukan pengguna.
4. Client mampu menerima pesan dari client lain (yang diteruskan oleh server), dan mencetaknya ke layar.
5. Client harus memasukkan password untuk dapat bergabung ke chatroom.
6. Client memiliki username yang unik.

# How to Run
1. Simpan kode server dalam file bernama server.py dan kode client dalam file bernama client.py.
2. Buka terminal atau command prompt, lalu jalankan perintah berikut: python server.py untuk menjalankan server dan python client.py untuk menjalankan client.
3. Jika server berhasil dijalankan, akan terihat pesan “Server is running and waiting for clients...” di GUI server.
4. Jika client berhasil dijalankan, GUI client akan terbuka dan meminta input untuk Server IP, Server Port (12345), Username, dan Password (udpudp).
5. Untuk menemukan IP Server, gunakan perintah ipconfig.
6. Klik login untuk mengakses chat room.
7. Jika berhasil, akan terlihat pesan “You have entered the chat room” yang menandakan bahwa client telah berhasil masuk ke chat room.

