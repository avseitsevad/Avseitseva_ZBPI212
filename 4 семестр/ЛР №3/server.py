import socket

sock = socket.socket()
sock.bind(('', 9090))
print("Запуск сервера...")
sock.listen(0)
print("Начало прослушивания порта...")

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