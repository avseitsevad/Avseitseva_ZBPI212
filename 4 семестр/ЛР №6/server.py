import socket
import os
from datetime import datetime
import threading
from config import PORT, MAX_BYTES, PATH

LOG_FILE = "server_logs.txt"

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

def handle_request(conn, addr):
    data = conn.recv(MAX_BYTES)
    request = data.decode()

    # Вывод информации о запросе в консоль
    print("Received request from:", addr)
    print("Request:")
    print(request)
    print()

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
        log_entry = "{}. {} - {} - 200".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), addr[0], request.split(' ')[1])

        try:
            conn.send(response.encode())
        except socket.error:
            print("Error: Failed to send response to", addr)
    else:
        # Отправка кода ошибки 404
        response = "HTTP/1.1 404 Not Found\r\nServer: SelfMadeServer v0.0.1\r\nConnection: close\r\n\r\n"
        log_entry = "{}. {} - {} - 404".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), addr[0], request.split(' ')[1])

        try:
            conn.send(response.encode())
        except socket.error:
            print("Error: Failed to send response to", addr)

    conn.close()

    # Запись лога в файл
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(log_entry + '\n')


def start_server():
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

        # Запуск обработки запроса в отдельном потоке
        thread = threading.Thread(target=handle_request, args=(conn, addr))
        thread.start()

if __name__ == '__main__':
    start_server()
