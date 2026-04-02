import socket
import random

HOST = "0.0.0.0"
PORT = 5555

code = str(random.randint(0, 999999)).zfill(6)
print(f"Join code: {code}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Waiting for client...")
conn, addr = server.accept()
print(f"Connected to: {addr}")

client_code = conn.recv(1024).decode()

if client_code == code:
    conn.send("OK".encode())

    data = "i'm server sending this to client"
    conn.send(data.encode())

    response = conn.recv(1024).decode()
    print(f"Received: {response}")
else:
    conn.send("INVALID".encode())

conn.close()
