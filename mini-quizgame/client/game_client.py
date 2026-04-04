import socket

from common.protocol import send, recv
from common.messages import MessageType


class GameClient:
    def __init__(self, host, port, nickname):
        self.host = host
        self.port = port
        self.nickname = nickname

        self.client = None

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 5555))

        self.send_join()
        self.listen()

    def listen(self):
        while True:
            msg = recv(self.client)

            if msg is None:
                break

            self.handle_message(msg)

    def handle_message(self, msg):
        msg_type = msg["type"]

        if msg_type == MessageType.PLAYER_LIST:
            self.handle_player_list(msg)

    def handle_player_list(self, msg):
        print("\nPlayers")
        for player in msg["players"]:
            print(f"- {player}")

    def send_join(self):
        join_data = {"type": MessageType.JOIN, "nickname": self.nickname}
        send(self.client, join_data)

    def send_answer(self, index):
        pass
