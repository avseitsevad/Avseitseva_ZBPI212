import socket
import threading
import os

log_file = os.path.join(os.path.dirname(__file__), 'log.txt')

host = 'localhost'
port = 9090

sock = socket.socket()

sock.bind((host, port))
with open(log_file, "a") as f:
    f.write("Запуск сервера...\n")
sock.listen(0)
with open(log_file, "a") as f:
    f.write("Начало прослушивания порта...\n")

print(f"Сервер слушает порт: {port}")

def handle_client(conn, addr):
    with open(log_file, "a") as f:
        f.write(f"Подключение клиента: {addr}\n")
        f.flush()

    msg = ''

    while True:
        data = conn.recv(1024)
        with open(log_file, "a") as f:
            f.write("Приём данных от клиента...\n")
            f.flush()
        if not data:
            break
        msg += data.decode()
        conn.send(data)
        with open(log_file, "a") as f:
            f.write("Отправка данных клиенту...\n")
            f.flush()

    with open(log_file, "a") as f:
        f.write(f"{msg}\n")
        f.flush()

    conn.close()
    with open(log_file, "a") as f:
        f.write("Отключение клиента...\n")
        f.flush()

while True:
    conn, addr = sock.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
