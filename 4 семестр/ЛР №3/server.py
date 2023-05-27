import socket

log_file = 'log.txt'

host_prompt = "Введите имя хоста (по умолчанию: localhost): "
port_prompt = "Введите номер порта (по умолчанию: 9090): "

default_host = 'localhost'
default_port = '9090'

host = input(host_prompt) or default_host
port = input(port_prompt) or default_port
port = int(port)

sock = socket.socket()
connected = False

while not connected:
    try:
        sock.bind((host, port))
        with open(log_file, "a") as f:
            f.write("Запуск сервера...\n")
        sock.listen(0)
        with open(log_file, "a") as f:
            f.write("Начало прослушивания порта...\n")
        connected = True
    except OSError:
        port += 1

print(f"Сервер слушает порт: {port}")

while True:
    conn, addr = sock.accept()
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
