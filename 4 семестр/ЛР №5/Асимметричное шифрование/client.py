import socket
import pickle
import rsa

host = 'localhost'
port = 8080

sock = socket.socket()
sock.connect((host, port))

# Загрузка публичного ключа сервера из файла
with open("server_public_key.txt", "rb") as f:
    server_pub_key = pickle.load(f)

# Ввод сообщения с клавиатуры
message = input("Введите сообщение для отправки на сервер: ")

# Шифрование сообщения с использованием публичного ключа сервера
msg_encrypted = rsa.encrypt(message.encode(), server_pub_key)

# Отправка зашифрованного сообщения на сервер
sock.send(pickle.dumps(msg_encrypted))
print('Отправлено сообщение:', message)

# Получение ответа от сервера
response = pickle.loads(sock.recv(1024))
print('Получен ответ от сервера:', response)

sock.close()
