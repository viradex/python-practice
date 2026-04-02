import socket
import random

HOST = "127.0.0.1"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind((HOST, PORT))

code = input("Enter join code: ")
client.send(code.encode())

response = client.recv(1024).decode()

if response == "OK":
    data = client.recv(1024).decode()
    print(f"Received: {data}")

    reply = "Yo whatsup"
    client.send(reply.encode())
else:
    print("Invalid code")

client.close()
