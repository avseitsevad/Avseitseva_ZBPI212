import socket
import pickle

def generate_keys(filename):
    # Генерация закрытого и открытого ключей
    p, g, a = 6, 5, 2
    A = (g ** a) % p
    keys = {'p': p, 'g': g, 'a': a, 'A': A}
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
    sock.connect((host, port))

    generate_keys('client_keys.txt')  # Генерация ключей и сохранение в файл

    with open('client_keys.txt', 'rb') as file:
        keys = pickle.load(file)
    A = keys['A']

    sock.send(pickle.dumps(A))

    B = pickle.loads(sock.recv(1024))
    K = (B ** keys['a']) % keys['p']
    key = str(K)

    message = input("Введите сообщение для отправки на сервер: ")
    msg_encrypted = encrypt_message(message, int(key) ^ B)
    sock.send(pickle.dumps((msg_encrypted, A)))
    print('Отправлено сообщение:', message)

    response, B = pickle.loads(sock.recv(1024))
    response_decoded = decrypt_message(response, int(key) ^ B)
    print('Получен ответ:', response_decoded)

    sock.close()

if __name__ == "__main__":
    main()
