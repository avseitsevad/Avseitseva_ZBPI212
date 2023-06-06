import socket

def get_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

sock = socket.socket()

sock.bind(('', 80))
print("Using port 80")

sock.listen(5)

conn, addr = sock.accept()
print("Connected", addr)

data = conn.recv(8192)
msg = data.decode()

print(msg)

request_parts = msg.split()
if len(request_parts) > 1:
    resource = request_parts[1]
    if resource == '/':
        resource = 'index.html'

    content = get_content(resource)
    resp = f"""HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

{content}"""

conn.send(resp.encode())

conn.close()
