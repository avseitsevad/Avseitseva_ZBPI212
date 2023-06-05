import socket
import pickle
import rsa
import os

host = 'localhost'
port = 8080

# Создание сокета и привязка к адресу
sock = socket.socket()
sock.bind((host, port))

# Запуск сервера
print("Запуск сервера")

# Начало прослушивания порта
sock.listen()
print("Начало прослушивания порта:", port)

# Подключение клиента
client_socket, client_address = sock.accept()
print("Подключение клиента:", client_address)

# Проверка наличия ключевых файлов
server_public_key_file = "server_public_key.txt"
server_private_key_file = "server_private_key.txt"
if not os.path.exists(server_public_key_file) or not os.path.exists(server_private_key_file):
    # Генерация новых ключей RSA
    (server_public_key, server_private_key) = rsa.newkeys(512)
    
    # Сохранение публичного и приватного ключей сервера в файлы
    with open(server_public_key_file, "wb") as f:
        pickle.dump(server_public_key, f)
    
    with open(server_private_key_file, "wb") as f:
        pickle.dump(server_private_key, f)
else:
    # Загрузка публичного и приватного ключей сервера из файлов
    with open(server_public_key_file, "rb") as f:
        server_public_key = pickle.load(f)
    
    with open(server_private_key_file, "rb") as f:
        server_private_key = pickle.load(f)

# Отправка публичного ключа сервера клиенту
client_socket.send(pickle.dumps(server_public_key))
print("Отправлен публичный ключ сервера")

# Получение зашифрованного сообщения от клиента
msg_encrypted = pickle.loads(client_socket.recv(1024))
print("Получено зашифрованное сообщение от клиента: ", msg_encrypted)

# Расшифровка сообщения с использованием приватного ключа сервера
message = rsa.decrypt(msg_encrypted, server_private_key).decode()
print("Расшифрованное сообщение:", message)

# Отправка ответа клиенту
response = "Сообщение получено"
response_encrypted = rsa.encrypt(response.encode(), server_public_key)
client_socket.send(pickle.dumps(response_encrypted))
print("Отправлен ответ клиенту")

# Отключение клиента
client_socket.close()
print("Клиент отключен")

# Остановка сервера
sock.close()
print("Сервер остановлен")
