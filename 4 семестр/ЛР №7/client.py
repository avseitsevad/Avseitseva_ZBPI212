import socket

HOST = 'localhost'
PORT = 6666

def save_file(filename, content):
    with open(filename, 'wb') as file:
        file.write(content)

while True:
    request = input('> ')
    
    if request == 'exit':
        break
    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    
    if request.startswith('download') and response != 'File not found':
        filename = request.split(' ', 1)[1]
        save_file(filename, sock.recv(1024))
        print('File downloaded successfully')
    
    sock.close()
