import socket
import pickle
import rsa

host = 'localhost'
port = 9090

sock = socket.socket()
sock.bind((host, port))
sock.listen(1)
conn, addr = sock.accept()

# Генерация публичного и приватного ключей
pub_key, priv_key = rsa.newkeys(512)

# Отправка публичного ключа клиенту
conn.send(pickle.dumps(pub_key))

# Получение зашифрованного сообщения от клиента
msg_encrypted = pickle.loads(conn.recv(1024))
print('Получено зашифрованное сообщение:', msg_encrypted)

# Расшифровка сообщения с использованием приватного ключа
msg_decrypted = rsa.decrypt(msg_encrypted, priv_key).decode()
print('Расшифрованное сообщение:', msg_decrypted)

conn.close()
