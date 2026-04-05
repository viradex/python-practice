import socket
import os
import threading

from common.protocol import send, recv
from common.messages import MessageType
from client.client_ui import ClientUI


class GameClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.nickname = None
        self.client = None

    def get_nickname(self):
        self.nickname = ClientUI.get_nickname()

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        ClientUI.join_server(self.host, self.port)
        self.send_join()

        ClientUI.cli_start("client")
        threading.Thread(target=self.client_input_loop, daemon=True).start()

        self.listen()

    def client_input_loop(self):
        while True:
            try:
                cmd = input("> ").strip()
            except EOFError:
                break

            if not cmd:
                continue

            self.handle_client_command(cmd)

    def listen(self):
        while True:
            msg = recv(self.client)

            if msg is None:
                break

            self.handle_message(msg)

    def handle_client_command(self, cmd: str):
        command, arg = ClientUI.parse_command(cmd)

        if command == "help":
            ClientUI.show_help()

        elif command == "list":
            print("Command disabled\n")

        elif command == "quit":
            self.leave_server()

        elif command == "error":
            print(arg + "\n")

        else:
            print("Invalid command. Type 'help' for available commands\n")

    def handle_message(self, msg):
        msg_type = msg["type"]

        if msg_type == MessageType.OTHER_JOIN:
            self.handle_other_join(msg)
        elif msg_type == MessageType.KICK:
            self.handle_kick(msg)
        elif msg_type == MessageType.OTHER_KICK:
            self.handle_other_kick(msg)
        elif msg_type == MessageType.OTHER_LEAVE:
            self.handle_other_leave(msg)
        elif msg_type == MessageType.SHUT_DOWN:
            self.handle_shut_down(msg)

    def handle_other_join(self, msg):
        ClientUI.player_joined(msg["nickname"])

    def handle_kick(self, msg):
        ClientUI.connection_lost(msg["reason"])

    def handle_other_kick(self, msg):
        ClientUI.player_kicked(msg["nickname"])

    def handle_shut_down(self, msg):
        ClientUI.connection_lost(msg["reason"])

    def handle_other_leave(self, msg):
        ClientUI.player_left(msg["nickname"])

    def send_join(self):
        send(self.client, {"type": MessageType.JOIN, "nickname": self.nickname})

    def send_answer(self, index):
        pass

    def leave_server(self):
        send(self.client, {"type": MessageType.LEAVE, "nickname": self.nickname})

        ClientUI.player_left(self.nickname)
        os._exit(0)
