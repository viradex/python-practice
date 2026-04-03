import json


def send(sock, data):
    msg = json.dumps(data) + "\n"
    sock.sendall(msg.encode())


def recv(sock):
    buffer = ""

    while "\n" not in buffer:
        chunk = sock.recv(4096).decode()
        if not chunk:
            return None

        buffer += chunk

    line, _, buffer = buffer.partition("\n")
    return json.loads(line)
