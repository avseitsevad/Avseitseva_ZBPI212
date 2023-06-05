import socket
import pickle
import rsa

host = 'localhost'
port = 8080

sock = socket.socket()
sock.connect((host, port))

# Получение публичного ключа сервера
server_pub_key = pickle.loads(sock.recv(1024))

# Ввод сообщения с клавиатуры
message = input("Введите сообщение для отправки на сервер: ")

# Шифрование сообщения с использованием публичного ключа сервера
msg_encrypted = rsa.encrypt(message.encode(), server_pub_key)

# Отправка зашифрованного сообщения на сервер
sock.send(pickle.dumps(msg_encrypted))
print('Отправлено сообщение:', message)

sock.close()
