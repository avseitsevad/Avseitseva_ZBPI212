import socket
import os
import shutil
import logging

# Создание и настройка логгера
logger = logging.getLogger('ftp_server')
logger.setLevel(logging.DEBUG)
log_file = 'server.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <dirname> - создает новую папку с указанным именем
rmdir <dirname> - удаляет папку с указанным именем
rm <filename> - удаляет файл с указанным именем
rename <oldname> <newname> - переименовывает файл с указанным именем на новое имя
upload <filename> - копирует файл с клиента на сервер
download <filename> - копирует файл с сервера на клиент
login <username> <password> - выполняет авторизацию пользователя
register <username> <password> - регистрирует нового пользователя
'''

# Указываем рабочую директорию для сервера
server_dir = os.getcwd()
users_dir = os.path.join(server_dir, 'users')
os.makedirs(users_dir, exist_ok=True)

# Файл с парами логин-пароль
users_file = os.path.join(server_dir, 'users.txt')

def process(req):
    if req == 'pwd':
        return os.getcwd()
    elif req == 'ls':
        return '; '.join(os.listdir(os.getcwd()))
    elif req.startswith('cat'):
        _, filename = req.split(' ', 1)
        try:
            with open(filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return 'File not found'
    elif req.startswith('mkdir'):
        _, dirname_new = req.split(' ', 1)
        try:
            os.mkdir(dirname_new)
            return 'Directory created successfully'
        except FileExistsError:
            return 'Directory already exists'
    elif req.startswith('rmdir'):
        _, dirname_remove = req.split(' ', 1)
        try:
            os.rmdir(dirname_remove)
            return 'Directory removed successfully'
        except FileNotFoundError:
            return 'Directory not found'
        except OSError:
            return 'Directory is not empty'
    elif req.startswith('rm'):
        _, filename_remove = req.split(' ', 1)
        try:
            os.remove(filename_remove)
            return 'File removed successfully'
        except FileNotFoundError:
            return 'File not found'
    elif req.startswith('rename'):
        _, oldname, newname = req.split(' ', 2)
        try:
            os.rename(oldname, newname)
            return 'File renamed successfully'
        except FileNotFoundError:
            return 'File not found'
        except FileExistsError:
            return 'File with the new name already exists'
    elif req.startswith('upload'):
        _, filename_upload = req.split(' ', 1)
        try:
            with open(filename_upload, 'rb') as file:
                shutil.copyfileobj(file, open(os.path.join(os.getcwd(), os.path.basename(filename_upload)), 'wb'))
            return 'File uploaded successfully'
        except FileNotFoundError:
            return 'File not found'
    elif req.startswith('download'):
        _, filename_download = req.split(' ', 1)
        try:
            with open(filename_download, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            return 'File not found'
    elif req.startswith('login'):
        _, username, password = req.split(' ', 2)
        if authenticate(username, password):
            return 'Authentication successful'
        else:
            logger.warning("Failed login attempt for user: %s", username)
            return 'Authentication failed'
    elif req.startswith('register'):
        _, username, password = req.split(' ', 2)
        if register_user(username, password):
            return 'Registration successful'
        else:
            return 'Registration failed'
    return 'bad request'

def authenticate(username, password):
    with open(users_file, 'r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(',')
            if username == stored_username and password == stored_password:
                return True
    return False

def register_user(username, password):
    with open(users_file, 'a') as file:
        file.write(f"{username},{password}\n")
    
    user_dir = os.path.join(users_dir, username)
    os.makedirs(user_dir, exist_ok=True)
    os.chdir(user_dir)
    
    return True


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
logger.info("Прослушиваем порт %d", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    logger.info("Request from %s: %s", addr[0], request)
    
    response = process(request)
    logger.info("Response to %s: %s", addr[0], response)
    
    conn.send(response.encode())

conn.close()
