import socket
import pickle

host = 'localhost'
port = 9091

sock = socket.socket()
sock.connect((host, port))

p, g, a = 6, 5, 2

# Вычисление публичного ключа клиента A
A = (g ** a) % p

# Отправка параметров p, g и публичного ключа A серверу
sock.send(pickle.dumps((p, g, A)))

# Получение публичного ключа сервера B
B = pickle.loads(sock.recv(1024))

# Вычисление общего секретного ключа K
K = (B ** a) % p
key = str(K)

# Ввод сообщения с клавиатуры
message = input("Введите сообщение для отправки на сервер: ")

# Шифрование сообщения с использованием общего секретного ключа
msg_encrypted = ""
for i in range(len(message)):
    char_code = ord(message[i])  # Получение кода символа
    encrypted_code = char_code ^ int(key)  # Применение операции XOR с ключом
    msg_encrypted += chr(encrypted_code)  # Преобразование обратно в символ

# Отправка зашифрованного сообщения на сервер
sock.send(pickle.dumps(msg_encrypted))
print('Отправлено сообщение:', message)

sock.close()
