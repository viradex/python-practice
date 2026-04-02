import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))
server.listen(5)
server.settimeout(1)  # accept() will timeout every 1 second

try:
    while True:
        try:
            client, addr = server.accept()
            print(client.recv(1024).decode())
            client.send("Hello from the server".encode())
            client.close()
        except socket.timeout:
            continue  # loop back to check for Ctrl+C
except KeyboardInterrupt:
    print("Server shutting down...")
    server.close()
