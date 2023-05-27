import socket

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
    print("Запуск сервера...")
    sock.listen(0)
    print("Начало прослушивания порта...")
except OSError as e:
    print(f"Не удалось запустить сервер. Проверьте правильность хоста и порта. Ошибка: {e}")

while True:
    conn, addr = sock.accept()
    print("Подключение клиента:", addr)

    msg = ''

    while True:
        data = conn.recv(1024)
        print("Приём данных от клиента...")
        if not data:
            break
        msg += data.decode()
        conn.send(data)
        print("Отправка данных клиенту...")

    print(msg)

    conn.close()
    print("Отключение клиента...")
print("Остановка сервера...")
