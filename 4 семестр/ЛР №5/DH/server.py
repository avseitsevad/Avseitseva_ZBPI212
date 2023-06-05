import socket
import pickle

host = 'localhost'
port = 9091

sock = socket.socket()
sock.bind((host, port))
sock.listen(1)
conn, addr = sock.accept()

# Получение параметров p, g и публичного ключа A от клиента
p, g, A = pickle.loads(conn.recv(1024))

# Генерация случайного секретного числа b для сервера
b = 4

# Вычисление публичного ключа сервера B
B = (g ** b) % p

# Отправка публичного ключа сервера B клиенту
conn.send(pickle.dumps(B))

# Вычисление общего секретного ключа K
K = (A ** b) % p

# Преобразование общего секретного ключа в строку
key = str(K)

# Получение зашифрованного сообщения от клиента
msg_encrypted = pickle.loads(conn.recv(1024))
print('Получено зашифрованное сообщение:', msg_encrypted)

# Расшифровка сообщения с использованием общего секретного ключа
msg_decoded = ""
for i in range(len(msg_encrypted)):
    encrypted_code = ord(msg_encrypted[i])  # Получение кода зашифрованного символа
    decrypted_code = encrypted_code ^ int(key)  # Применение операции XOR с ключом
    msg_decoded += chr(decrypted_code)  # Преобразование обратно в символ

print('Расшифрованное сообщение:', msg_decoded)

conn.close()
