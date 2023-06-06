import socket
import os
from datetime import datetime

# Загрузка настроек из файла config.py
try:
    from config import PORT, MAX_BYTES, PATH
except ImportError:
    print("Error: config.py file not found.")
    exit()

def get_content(file_path):
    # Чтение содержимого файла
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def get_response(request):
    # Парсинг запроса и определение пути ресурса
    request_lines = request.split('\r\n')
    if len(request_lines) > 0:
        request_parts = request_lines[0].split(' ')
        if len(request_parts) > 1:
            resource_path = request_parts[1]
            if resource_path == '/':
                resource_path = '/index.html'  # Если не указан ресурс, используем index.html

            file_path = os.path.join(PATH, resource_path[1:])  # Убираем первый слэш из пути ресурса
            if os.path.exists(file_path):
                return get_content(file_path)
    return ''

sock = socket.socket()

try:
    sock.bind(('', PORT))
    print("Using port", PORT)
except OSError:
    print("Error: Port", PORT, "is already in use.")
    exit()

sock.listen(5)

while True:
    conn, addr = sock.accept()
    print("Connected", addr)

    data = conn.recv(MAX_BYTES)
    request = data.decode()

    print(request)

    response_content = get_response(request)

    if response_content:
        # Формирование заголовков ответа
        headers = [
            "HTTP/1.1 200 OK",
            "Server: SelfMadeServer v0.0.1",
            "Content-type: text/html",
            "Connection: close",
            "Content-length: {}".format(len(response_content)),
            "Date: {}".format(datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))
        ]

        response = "\r\n".join(headers) + "\r\n\r\n" + response_content
    else:
        # Отправка кода ошибки 404
        response = "HTTP/1.1 404 Not Found\r\nServer: SelfMadeServer v0.0.1\r\nConnection: close\r\n\r\n"

    conn.send(response.encode())
    conn.close()
