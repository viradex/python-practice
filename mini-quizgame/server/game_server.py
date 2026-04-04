import socket
import sys
import select

from server.game_state import GameState
from common.protocol import send, recv
from common.messages import MessageType


class GameServer:
    """This class manages the server: initializing it, running the game, and handling clients."""

    def __init__(
        self, host: str, port: int, questions: list[dict[str, str | int | list[str]]]
    ) -> None:
        """
        Initialize the game server. This does not start the server or start accepting clients.

        Parameters:
            host (str): The host IP address. For example, set it to `0.0.0.0` to listen to all network interfaces on the machine, or `127.0.0.1` to make it only accessible on this local machine.
            port (int): The port to listen to on the IP address. Set this to an unreserved port, generally anything above `1024`.
            questions (list): A list containing dictionaries for each individual question's information.
        """

        self.host = host
        self.port = port
        self.questions = questions

        self.clients: list[socket.socket] = []
        self.client_names: dict[socket.socket, str] = {}
        self.state = GameState()
        self.server: socket.socket = None

    def start(self) -> None:
        """
        Start the server, making it available on the network and listen for incoming requests (such as from clients).

        This method creates a TCP socket and listens on the provided host at the provided port, reserving it.
        Clients are not accepted by this method; they will be added to a backlog queue until `accept_clients()` is called.
        """

        # TCP over UDP, for reliability
        # Latency is not as important
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.server.settimeout(1.0)

        # TODO should this stay?
        print(f"Started server, listening on {self.host} on port {self.port}")

    def accept_clients(self) -> None:
        """
        Starts waiting for incoming connections from clients, once the server has been created and started using `start()`.
        Once a client connects, the server listens for any messages from that client and handles them accordingly.

        Handles a `KeyboardInterrupt` by shutting down the server.
        """

        try:
            while True:
                try:
                    client, addr = self.server.accept()
                except socket.timeout:
                    continue

                client.settimeout(1.0)
                self.clients.append(client)

                print(f"Client joined (IP {addr[0]}:{addr[1]})\n")
                self.listen(client)
        except KeyboardInterrupt:
            self.shutdown()

    def listen(self, client: socket.socket) -> None:
        """
        Listens for any incoming messages from the client provided, forever. If the client disconnects,
        the loop is broken and a message is outputted. Handles any valid messages appropriately using `handle_message()`.

        Only accepts serialized JSON data from the client.

        Handles a `KeyboardInterrupt` by disconnecting the client from the server.

        Parameters:
            client (socket): The client to listen to for incoming messages.
        """

        try:
            while True:
                try:
                    msg = recv(client)
                except socket.timeout:
                    continue

                if msg is None:
                    print("Client disconnected")
                    break

                self.handle_message(client, msg)
        except KeyboardInterrupt:
            print("\nDisconnected client from server")
        finally:
            client.close()

    def handle_message(self, client: socket.socket, msg: dict) -> None:
        """
        Handle messages from the server appropriately by matching the `type` key in the dictionary
        from the message to any valid value in `MessageType`.

        Parameters:
            client (socket): The client that sent the message.
            msg (dict): A dictionary containing the data that the client sent. Must include the `type` key.
        """
        msg_type = msg["type"]

        if msg_type == MessageType.JOIN:
            self.handle_join(client, msg)

    def handle_join(self, client: socket.socket, msg: dict[str, str]) -> None:
        """
        Handles a `JOIN` message type.

        Adds the player to the `GameState` and outputs a message to the console.
        Also broadcasts a message to all clients about the updated player list.

        Parameters:
            client (socket): The client that sent the message.
            msg (dict): A dictionary containing the data that the client sent.
        """
        nickname = msg["nickname"]

        self.state.add_player(nickname)
        print(f"{nickname} joined the game")

        all_players_data = {
            "type": MessageType.PLAYER_LIST,
            "players": list(self.state.players.keys()),
        }
        self.broadcast(all_players_data)

    def broadcast(self, msg: dict) -> None:
        """
        Send a message to all clients that are currently connected to the server.

        Parameters:
            msg (dict): A dictionary containing the message to send to all clients. Must contain the `type` key.
        """

        for client in self.clients:
            send(client, msg)

    def run_game(self):
        pass

    def ask_question(self, question):
        pass

    def collect_answers(self):
        pass

    def calculate_scores(self):
        pass

    def shutdown(self) -> None:
        """Shut down the server and disconnect any and all clients currently connected to the server."""

        for client in self.clients:
            try:
                client.close()
            except OSError:
                pass  # Socket already closed or invalid

        if self.server:
            try:
                self.server.close()
            except OSError:
                pass

        print("Server has been shut down\n")
