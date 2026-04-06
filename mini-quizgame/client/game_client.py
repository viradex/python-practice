import socket
import sys
import threading

from common.protocol import send, recv
from common.messages import MessageType
from client.client_ui import ClientUI


class GameClient:
    def __init__(self, port):
        self.port = port
        self.host = None

        self.nickname = None
        self.client = None

        self.in_game = False
        self.answered = False
        self.awaiting_player_list = False

    def get_ip_address(self):
        self.host = ClientUI.get_ip_address()

    def get_nickname(self):
        self.nickname = ClientUI.get_nickname()

    def connect(self):
        if self.host is None or self.nickname is None:
            raise ValueError(
                "host and nickname must have values, call get_ip_address() and get_nickname() before connecting"
            )

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
        except ConnectionRefusedError:
            print(
                f"\nThe server could not be found (tried connecting to {self.host}:{self.port} but the connection was refused).\n"
            )
            sys.exit(1)

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
            self.ask_player_list()

        elif command == "answer":
            self.send_answer(arg)

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
        elif msg_type == MessageType.PLAYER_LIST:
            self.handle_player_list(msg)
        elif msg_type == MessageType.SHUT_DOWN:
            self.handle_shut_down(msg)
        elif msg_type == MessageType.STARTING:
            self.handle_starting(msg)
        elif msg_type == MessageType.QUESTION:
            self.handle_question(msg)
        elif msg_type == MessageType.ANSWER_RESULT:
            self.handle_answer_result(msg)
        elif msg_type == MessageType.GAME_OVER:
            self.handle_game_over(msg)

    def handle_other_join(self, msg):
        ClientUI.player_joined(msg["nickname"])

    def handle_kick(self, msg):
        ClientUI.connection_lost(msg["reason"])

    def handle_other_kick(self, msg):
        ClientUI.player_kicked(msg["nickname"])

    def handle_other_leave(self, msg):
        if msg["nickname"] != self.nickname:
            ClientUI.player_left(msg["nickname"])

    def handle_player_list(self, msg):
        if self.awaiting_player_list:
            ClientUI.show_players(msg["players"])

        self.awaiting_player_list = False

    def handle_shut_down(self, msg):
        ClientUI.connection_lost(msg["reason"])

    def handle_starting(self, msg):
        print("Starting game...\n")
        self.in_game = True

    def handle_question(self, msg):
        if self.in_game:
            self.answered = False
            ClientUI.show_question(msg["number"], msg["question"], msg["choices"])

    def handle_answer_result(self, msg):
        if msg["result"] == "correct":
            print("You got it right!\n")
        else:
            letters = ("A", "B", "C", "D")
            print(f"Wrong! The correct answer was {letters[msg["correct_index"]]}\n")

    def handle_game_over(self, msg):
        self.in_game = False
        ClientUI.show_scores(msg["scores"])

    def send_answer(self, answer):
        if not self.in_game:
            print("This command can only be run once the game has started\n")
            return

        elif self.answered:
            print("You already answered\n")
            return

        valid_answers = ["a", "b", "c", "d"]
        answer = answer.lower().strip()

        if answer not in valid_answers:
            print("Invalid answer\n")
            return

        send(
            self.client,
            {"type": MessageType.ANSWER, "answer": valid_answers.index(answer)},
        )
        self.answered = True

        print("Answered!\n")

    def ask_player_list(self):
        self.awaiting_player_list = True
        send(self.client, {"type": MessageType.PLAYER_LIST})

    def send_join(self):
        send(self.client, {"type": MessageType.JOIN, "nickname": self.nickname})

    def leave_server(self):
        send(self.client, {"type": MessageType.LEAVE, "nickname": self.nickname})

        ClientUI.player_left(self.nickname)
        sys.exit(0)
