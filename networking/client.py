import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

client.send("Hello from the client".encode())
print(client.recv(1024).decode())
