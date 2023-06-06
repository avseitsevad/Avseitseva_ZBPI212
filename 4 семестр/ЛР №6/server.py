import socket
import threading
import os
from datetime import datetime
import mimetypes
import config

HOST = ''
PORT = config.PORT
MAX_BYTES = config.MAX_BYTES
WORKING_DIRECTORY = config.PATH
LOG_FILE = 'server_logs.txt'
ALLOWED_FILE_TYPES = config.ALLOWED_FILE_TYPES  # Разрешенные типы файлов

def get_response(request):
    request_parts = request.split('\r\n')
    request_line = request_parts[0].split(' ')
    method = request_line[0]
    file_path = request_line[1]

    if file_path == '/':
        file_path = '/index.html'

    file_extension = os.path.splitext(file_path)[1]

    if file_extension.lower() not in ALLOWED_FILE_TYPES:
        return generate_error_response(403)  # Ошибка 403 - запрещено

    file_path = WORKING_DIRECTORY + file_path

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
            return content
    else:
        return generate_error_response(404)  # Ошибка 404 - файл не найден

def generate_error_response(error_code):
    error_message = {
        403: 'Forbidden',
        404: 'Not Found'
    }

    response = "HTTP/1.1 {} {}\r\nServer: SelfMadeServer v0.0.1\r\nConnection: close\r\n\r\n".format(
        error_code, error_message.get(error_code, ''))
    return response.encode()

def handle_request(conn, addr):
    data = conn.recv(MAX_BYTES)
    request = data.decode()

    # Вывод информации о запросе в консоль
    print("Received request from:", addr)
    print("Request:")
    print(request)
    print()

    response_content = get_response(request)

    headers = [
        "HTTP/1.1 200 OK",
        "Server: SelfMadeServer v0.0.1",
        "Content-type: {}".format(mimetypes.guess_type(request.split(' ')[1])[0] or 'application/octet-stream'),
        "Connection: close",
        "Content-length: {}".format(len(response_content)),
        "Date: {}".format(datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))
    ]

    if response_content.startswith(b"HTTP/1.1 4"):
        # Обработка ошибки 4xx (403, 404 и др.)
        headers[0] = response_content.split(b'\r\n')[0].decode()  # Заменяем статусный код и сообщение
        response_content = b''

    response = "\r\n".join(headers).encode() + b"\r\n\r\n" + response_content

    try:
        conn.send(response)
    except socket.error:
        print("Error: Failed to send response to", addr)

    conn.close()

    # Запись лога в файл
    log_entry = "{}. {} - {} - {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), addr[0], request.split(' ')[1], headers[0].split(' ')[1])
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(log_entry + '\n')

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind((HOST, PORT))
        print("Using port", PORT)
    except OSError as e:
        print("Error: Failed to bind the socket:", e)
        return

    sock.listen(5)
    print("Server started on {}:{}".format(HOST, PORT))
    print("Working directory:", WORKING_DIRECTORY)
    print("Press Ctrl+C to stop the server.")

    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=handle_request, args=(conn, addr))
        thread.start()

start_server()
