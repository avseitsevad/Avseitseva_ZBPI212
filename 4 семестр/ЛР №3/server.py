import socket

log_file = "log.txt"

host_prompt = "Введите имя хоста (по умолчанию: localhost): "
port_prompt = "Введите номер порта (по умолчанию: 9090): "

default_host = 'localhost'
default_port = '9090'

host = input(host_prompt) or default_host
port = input(port_prompt) or default_port
port = int(port)

sock = socket.socket()
try:
    sock.bind((host, port))
    with open(log_file, "a") as f:
        f.write("Запуск сервера...\n")
    sock.listen(0)
    with open(log_file, "a") as f:
        f.write("Начало прослушивания порта...\n")
except OSError as e:
    with open(log_file, "a") as f:
        f.write(f"Не удалось запустить сервер. Проверьте правильность хоста и порта. Ошибка: {e}\n")

while True:
    conn, addr = sock.accept()
    with open(log_file, "a") as f:
        f.write(f"Подключение клиента: {addr}\n")

    msg = ''

    while True:
        data = conn.recv(1024)
        with open(log_file, "a") as f:
            f.write("Приём данных от клиента...\n")
        if not data:
            break
        msg += data.decode()
        conn.send(data)
        with open(log_file, "a") as f:
            f.write("Отправка данных клиенту...\n")

    with open(log_file, "a") as f:
        f.write(f"{msg}\n")

    conn.close()
    with open(log_file, "a") as f:
        f.write("Отключение клиента...\n")
        
with open(log_file, "a") as f:
    f.write("Остановка сервера...\n")