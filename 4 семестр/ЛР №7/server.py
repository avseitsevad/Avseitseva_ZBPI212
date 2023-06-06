import socket
import os
import shutil

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
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    elif req.startswith('cat'):
        _, filename = req.split(' ', 1)
        try:
            with open(os.path.join(dirname, filename), 'r') as file:
                return file.read()
        except FileNotFoundError:
            return 'File not found'
    elif req.startswith('mkdir'):
        _, dirname_new = req.split(' ', 1)
        try:
            os.mkdir(os.path.join(dirname, dirname_new))
            return 'Directory created successfully'
        except FileExistsError:
            return 'Directory already exists'
    elif req.startswith('rmdir'):
        _, dirname_remove = req.split(' ', 1)
        try:
            os.rmdir(os.path.join(dirname, dirname_remove))
            return 'Directory removed successfully'
        except FileNotFoundError:
            return 'Directory not found'
        except OSError:
            return 'Directory is not empty'
    elif req.startswith('rm'):
        _, filename_remove = req.split(' ', 1)
        try:
            os.remove(os.path.join(dirname, filename_remove))
            return 'File removed successfully'
        except FileNotFoundError:
            return 'File not found'
    elif req.startswith('rename'):
        _, oldname, newname = req.split(' ', 2)
        try:
            os.rename(os.path.join(dirname, oldname), os.path.join(dirname, newname))
            return 'File renamed successfully'
        except FileNotFoundError:
            return 'File not found'
        except FileExistsError:
            return 'File with the new name already exists'
    elif req.startswith('upload'):
        _, filename_upload = req.split(' ', 1)
        try:
            with open(filename_upload, 'rb') as file:
                shutil.copyfileobj(file, open(os.path.join(dirname, os.path.basename(filename_upload)), 'wb'))
            return 'File uploaded successfully'
        except FileNotFoundError:
            return 'File not found'
    elif req.startswith('download'):
        _, filename_download = req.split(' ', 1)
        try:
            with open(os.path.join(dirname, filename_download), 'rb') as file:
                return file.read()
        except FileNotFoundError:
            return 'File not found'
    return 'bad request'


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())

conn.close()
