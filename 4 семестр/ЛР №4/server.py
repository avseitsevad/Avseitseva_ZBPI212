import socket
import threading
import os
import sys

log_file = os.path.join(os.path.dirname(__file__), 'log.txt')
auth_file = os.path.join(os.path.dirname(__file__), 'auth.txt')

host = 'localhost'
port = 9090

sock = socket.socket()
sock.bind((host, port))
sock.listen(0)

print(f"Сервер слушает порт: {port}")

# Флаги для управления сервером
running = True
paused = False

# Блокировка для синхронизации доступа к флагам
flags_lock = threading.Lock()

# Блокировка для синхронизации доступа к файлам
files_lock = threading.Lock()

# Функция для обработки подключения клиента
def handle_client(conn, addr):
    with files_lock:
        with open(log_file, "a") as f:
            f.write(f"Подключение клиента: {addr}\n")
            f.flush()

    msg = ''

    while True:
        data = conn.recv(1024)
        with files_lock:
            with open(log_file, "a") as f:
                f.write("Приём данных от клиента...\n")
                f.flush()
        if not data:
            break
        msg += data.decode()
        conn.send(data)
        with files_lock:
            with open(log_file, "a") as f:
                f.write("Отправка данных клиенту...\n")
                f.flush()

    with files_lock:
        with open(log_file, "a") as f:
            f.write(f"{msg}\n")
            f.flush()

    conn.close()
    with files_lock:
        with open(log_file, "a") as f:
            f.write("Отключение клиента...\n")
            f.flush()

# Функция для остановки сервера
def stop_server():
    global running
    with flags_lock:
        running = False
    print('Отключение сервера...')

# Функция для приостановки прослушивания порта
def pause_server():
    global paused
    with flags_lock:
        paused = True

# Функция для возобновления прослушивания порта
def resume_server():
    global paused
    with flags_lock:
        paused = False

# Функция для вывода логов
def show_logs():
    with files_lock:
        with open(log_file, "r") as f:
            logs = f.read()
    print(logs)

# Функция для очистки логов
def clear_logs():
    with files_lock:
        with open(log_file, "w") as f:
            pass
    print("Логи очищены.")

# Функция для очистки файла идентификации
def clear_auth_file():
    with files_lock:
        with open(auth_file, "w") as f:
            pass
    print("Файл идентификации очищен.")

# Функция для обработки команд пользователя
def handle_commands():
    while True:
        command = input("Введите команду (stop/pause/resume/logs/clear_logs/clear_auth_file): ")
        if command == "stop":
            stop_server()
            break
        elif command == "pause":
            pause_server()
        elif command == "resume":
            resume_server()
        elif command == "logs":
            show_logs()
        elif command == "clear_logs":
            clear_logs()
        elif command == "clear_auth_file":
            clear_auth_file()

# Функция для запуска сервера
def run_server():
    global running
    global paused

    while True:
        conn, addr = sock.accept()

        with flags_lock:
            if not running:
                break
            if paused:
                continue

        threading.Thread(target=handle_client, args=(conn, addr)).start()

    sock.close()

# Запуск управляющего потока для обработки команд пользователя
threading.Thread(target=handle_commands).start()

# Запуск сервера
run_server()
