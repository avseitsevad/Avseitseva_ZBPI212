import socket
import pickle

def generate_keys(filename):
    # Генерация закрытого и открытого ключей
    p, g, b = 6, 5, 4
    B = (g ** b) % p
    keys = {'p': p, 'g': g, 'b': b, 'B': B}
    with open(filename, 'wb') as file:
        pickle.dump(keys, file)

def encrypt_message(message, key):
    encrypted_message = ""
    for i in range(len(message)):
        char_code = ord(message[i])
        encrypted_code = char_code ^ key
        encrypted_message += chr(encrypted_code)
    return encrypted_message

def decrypt_message(encrypted_message, key):
    decrypted_message = ""
    for i in range(len(encrypted_message)):
        encrypted_code = ord(encrypted_message[i])
        decrypted_code = encrypted_code ^ key
        decrypted_message += chr(decrypted_code)
    return decrypted_message

def main():
    host = 'localhost'
    port = 9091

    sock = socket.socket()
    sock.bind((host, port))
    print('Запуск сервера...')
    sock.listen(1)
    print('Начало прослушивания порта', port)

    conn, addr = sock.accept()
    print('Подключение клиента:', addr)

    generate_keys('server_keys.txt')  # Генерация ключей и сохранение в файл

    with open('server_keys.txt', 'rb') as file:
        keys = pickle.load(file)
    B = keys['B']

    conn.send(pickle.dumps(B))
    print('Отправлен открытый ключ сервера B:', B)

    A = pickle.loads(conn.recv(1024))
    K = (A ** keys['b']) % keys['p']
    key = str(K)

    msg_encrypted, A = pickle.loads(conn.recv(1024))
    msg_decoded = decrypt_message(msg_encrypted, int(key) ^ A)
    print('Сообщение расшифровано:', msg_decoded)

    response = "Сообщение получено и расшифровано"
    response_encrypted = encrypt_message(response, int(key) ^ A)
    conn.send(pickle.dumps((response_encrypted, B)))
    print('Отправлен зашифрованный ответ:', response_encrypted)

    conn.close()
    print('Отключение клиента')

    sock.close()
    print('Остановка сервера')

if __name__ == "__main__":
    main()
