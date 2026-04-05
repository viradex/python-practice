import socket
import os
import threading

from server.game_state import GameState
from server.server_ui import ServerUI
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

        self.running = False
        self.clients: list[socket.socket] = []
        self.client_names: dict[socket.socket, str] = {}
        self.state = GameState()
        self.server: socket.socket = None

    def _remove_client(self, client, nickname):
        client.close()
        self.clients.remove(client)

        del self.client_names[client]
        del self.state.players[nickname]

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

        self.running = True
        self.server.settimeout(1.0)

        ServerUI.start_server(self.host, self.port)

    def accept_clients(self) -> None:
        """
        Starts waiting for incoming connections from clients, once the server has been created and started using `start()`.
        Once a client connects, the server listens for any messages from that client and handles them accordingly.

        Handles a `KeyboardInterrupt` by shutting down the server.
        """

        ServerUI.cli_start("server")
        threading.Thread(target=self.host_input_loop).start()

        try:
            while self.running:
                try:
                    client, addr = self.server.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break

                client.settimeout(1.0)
                self.clients.append(client)

                print(f"Client joined (IP {addr[0]}:{addr[1]})")
                threading.Thread(target=self.listen, args=(client,)).start()
        except KeyboardInterrupt:
            self.shutdown()

    def host_input_loop(self):
        while self.running:
            try:
                cmd = input("> ").strip()
            except EOFError:
                break

            if not cmd:
                continue

            self.handle_server_command(cmd)

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
            while self.running:
                try:
                    msg = recv(client)
                except socket.timeout:
                    continue
                except OSError:
                    break

                if msg is None:
                    print("Client disconnected")
                    break

                self.handle_message(client, msg)
        except KeyboardInterrupt:
            print("\nDisconnected client from server")
        finally:
            client.close()

    def handle_server_command(self, cmd: str):
        command, arg = ServerUI.parse_command(cmd)

        if command == "help":
            ServerUI.show_help()

        elif command == "start":
            self.run_game()

        elif command == "list":
            ServerUI.show_players(self.state.players)

        elif command == "kick":
            self.kick_player(arg, "You were kicked by the host")

        elif command == "stop":
            self.shutdown()

        elif command == "error":
            print(arg + "\n")

        else:
            print("Invalid command. Type 'help' for available commands\n")

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
        elif msg_type == MessageType.LEAVE:
            self.handle_leave(client, msg)

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

        if nickname in self.client_names.values():
            print(f"A player with the name {nickname} already exists\n")

            # Send KICK message to the new client only
            try:
                send(
                    client,
                    {
                        "type": MessageType.KICK,
                        "reason": "A player with the same name is already on the server!",
                    },
                )
                client.shutdown(socket.SHUT_RDWR)  # Flush the message
            except OSError:
                pass
            finally:
                client.close()

            # Remove the new client from the list if added
            if client in self.clients:
                self.clients.remove(client)

            return

        self.client_names[client] = nickname

        self.state.add_player(nickname)
        ServerUI.player_joined(nickname)

        self.broadcast(
            {
                "type": MessageType.OTHER_JOIN,
                "nickname": nickname,
            }
        )

    def handle_leave(self, client, msg):
        name = msg["nickname"]

        ServerUI.player_left(name)
        self.broadcast({"type": MessageType.OTHER_LEAVE, "nickname": name})

        self._remove_client(client, name)

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

    def kick_player(self, name: str, reason: str):
        for client, n in list(self.client_names.items()):
            if n == name:
                ServerUI.player_kicked(name)

                self.broadcast({"type": MessageType.OTHER_KICK, "nickname": name})
                send(
                    client,
                    {"type": MessageType.KICK, "reason": reason},
                )

                self._remove_client(client, name)
                return

        print(f"The player {name} does not exist\n")

    def shutdown(self) -> None:
        """Shut down the server and disconnect any and all clients currently connected to the server."""
        self.broadcast({"type": MessageType.SHUT_DOWN, "reason": "Server closed"})

        self.running = False

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

        ServerUI.server_shutdown()
        os._exit(0)
