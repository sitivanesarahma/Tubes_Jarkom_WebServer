# Implementasi pembuatan TCP socket dan mengaitkannya ke alamat dan port tertentu
from socket import * # mengimport socket

def tcp_server():
    serverHost = 'localhost' # server host yang digunakan adalah local host
    serverPort = 80 # server port yang digunakan adalah port 80
    serverSocket = socket(AF_INET, SOCK_STREAM) # membuat objek socket untuk protokol TCP dengan menggunakan modul socket
    serverSocket.bind((serverHost, serverPort)) # mengaitkan TCP ke alamat host/port tertentu
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # memungkinkan socket untuk menggunakan kembali alamat dan port yang sama yang digunakan sebelumnya meskipun belum sepenuhnya dilepaskan oleh kernel
    serverSocket.listen(1) # mengatur socket untuk menerima koneksi dari klien
    print('The Server is Ready to Receive') # mencetak kalimat 'The Server is Ready to Receive' apabila socket berhasil dibuat

    while True:
        # Establish the connection
        connectionSocket, addr = serverSocket.accept() 
        try:
            # Parsing HTTP request dengan membaca pesan HTTP dari soket, kemudian memecah pesan tersebut ke dalam metode permintaan dan path permintaan.
            message = connectionSocket.recv(1024).decode() # menerima pesan dari client melalui koneksi soket dengan ukuran maksimum 1024 byte, kemudian mengubah byte menjadi string 
            print("message from client: " + message) # mencetak pesan yang diterima dari klien ke konsol. Pesan tersebut merupakan pesan HTTP yang dikirim oleh klien.
            request_method = message.split(' ')[0] # memisahkan pesan HTTP menjadi beberapa bagian dengan menggunakan spasi (' ') sebagai pemisah. Kemudian, elemen pertama (indeks 0) dari hasil pemisahan tersebut disimpan dalam variabel request_method. Dalam konteks HTTP, elemen pertama biasanya merupakan metode permintaan, seperti "GET", "POST", dll.
            request_path = message.split(' ')[1] # melakukan hal yang sama seperti baris sebelumnya, tetapi kali ini elemen kedua (indeks 1) dari hasil pemisahan disimpan dalam variabel request_path. Dalam konteks HTTP, elemen kedua umumnya merupakan jalur permintaan, seperti "/index.html"

            # Jika method adalah GET, maka path request akan diambil sebagai argumen untuk memanggil fungsi handle_request(); method GET digunakan untuk mendapatkan data atau konten dari server
            if request_method == 'GET':
                if request_path == '/':
                    # Mengirimkan respon default
                    response = handle_request('index.html')
                else:
                    try:
                        # cek jika file ada dan kirim tanggapan yang sesuai
                        if request_path.endswith('.html'): # cek file dalam tipe konten html
                            content_type = 'text/html'
                        elif request_path.endswith('.css'): # cek file dalam tipe konten css
                            content_type = 'text/css'
                        elif request_path.endswith('.js'): # cek file dalam tipe konten js
                            content_type = 'application/javascript'
                        elif request_path.endswith('.jpg') or request_path.endswith('.jpeg'): # cek file dalam tipe konten jpg atau jpeg untuk gambar
                            content_type = 'image/jpeg'
                        elif request_path.endswith('.png'): # cek file dalam tipe konten png untuk gambar
                            content_type = 'image/png'
                        elif request_path.endswith('.woff2'): # cek file dalam tipe konten woff2 untuk bentuk tulisan
                            content_type = 'font/woff2'
                        else: # cek file dalam tipe konten text yang plain seperti notepad, dll
                            content_type = 'text/plain' 
                            
                        file = open(request_path[1:], 'rb') # membuka file yang di request
                        file_content = file.read() # membaca file
                        file.close() # menutup file
                        response_header = "HTTP/1.1 200 OK\r\n" # berisi status line dari respon HTTP dari protokol (HTTP 1.1) yang apabila berhasil akan mengeluarkan kode status 200 OK
                        content_type_header = "Content-Type: " + content_type + "\r\n" # berisi header "Content-Type" dari respon HTTP. conten-type adalah tipe konten yang ingin dikirimkan ke klien
                        content_length_header = "Content-Length: " + str(len(file_content)) + "\r\n" # berisi header "Content-Length" dari respon HTTP. Nilai len(file_content) adalah panjang (jumlah byte) dari file_content, yang merupakan isi dari file yang akan dikirimkan ke klien.
                        response = response_header + content_type_header + content_length_header + "\r\n" # berisi respon HTTP lengkap, yang terdiri dari status line (response_header), header "Content-Type" (content_type_header), header "Content-Length" (content_length_header), dan karakter akhir baris tambahan (\r\n).
                        response_bytes = bytes(response, 'utf-8') + file_content # berisi respon HTTP lengkap dalam bentuk byte. Pertama, string response diubah menjadi objek byte menggunakan metode bytes(), dengan encoding 'utf-8'. Kemudian, konten file (file_content) ditambahkan ke respon HTTP dalam bentuk byte.
                        connectionSocket.sendall(response_bytes) # untuk mengirimkan seluruh byte dari response_bytes kepada klien melalui koneksi socket.
                    except FileNotFoundError:
                        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>\r\n" # respon apabila file tidak ditemukan pada penyimpanan direktori yang sama dengan server
            else:
                response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\n<html><body><h1>405 Method Not Allowed</h1></body></html>\r\n" # respon apabila metode yang digunakan tidak diizinikan oleh server, seperti metode post atau put

            connectionSocket.sendall(response.encode()) # Mengirimkan seluruh response message

        except IOError:
            connectionSocket.send("HTTP/1/1 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode()) # mengirimkan respon apabila konten tidak ditemukan di server
            connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode()) # mengirimkan respon apabila konten tidak ditemukan di server

        connectionSocket.close() # Menutup Koneksi

# Fungsi untuk membaca file yang diminta dan menghasilkan respon HTTP 200 OK dengan tipe konten yang sesuai
def handle_request(file_path):
    file = open(file_path, 'rb') # membuka file sesuai path yang diminta
    file_content = file.read() # membaca file
    file.close() # menutup file
    response_header = "HTTP/1.1 200 OK\r\n" # berisi status line dari respon HTTP dari protokol (HTTP 1.1) yang apabila berhasil akan mengeluarkan kode status 200 OK
    content_type_header = "Content-Type: text/html\r\n" # berisi header "Content-Type" dari respon HTTP. conten-type adalah tipe konten yang ingin dikirimkan ke klien
    content_length_header = "Content-Length: " + str(len(file_content)) + "\r\n" # berisi header "Content-Length" dari respon HTTP. Nilai len(file_content) adalah panjang (jumlah byte) dari file_content, yang merupakan isi dari file yang akan dikirimkan ke klien.
    response = response_header + content_type_header + content_length_header + "\r\n" + file_content.decode() # menggabungkan semua elemen respon HTTP menjadi satu string yang lengkap ditambah dengan hasil dari pengubahan file_content dari bentuk byte menjadi string menggunakan metode decode()
    return response # mengembalikan nilai respon

if __name__ == "__main__": 
    tcp_server() # memanggil fungsi tcp server untuk dijalankan sebagai program utama