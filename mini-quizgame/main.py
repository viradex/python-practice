from server.game_server import GameServer
from client.game_client import GameClient
from utils.json_loader import JSONLoader

# TODO maybe temporary consts?
SERVER_IP = "0.0.0.0"
CLIENT_IP = "127.0.0.1"
PORT = 5555


def host_game() -> None:
    """Start the server for hosting the game and handling clients."""

    questions = JSONLoader().load_all()
    server = GameServer(SERVER_IP, PORT, questions)

    # TODO in GameServer init?
    server.start()
    server.accept_clients()


def join_game() -> None:
    """Start the program as a client to join a server."""

    # TODO nickname prompt should be in CLIUI class
    nickname = input("Enter nickname: ")
    client = GameClient(CLIENT_IP, PORT, nickname)

    # TODO in GameClient init?
    client.connect()


def main() -> None:
    """Start the program with a prompt to ask whether to start the program as a server or client."""

    print("Would you like to...\n1. Host game\n2. Join game\n")
    while True:
        choice = input("Enter choice (or blank to exit): ").strip()

        if choice == "1":
            host_game()
        elif choice == "2":
            join_game()
        elif choice == "":
            print("Exiting...")
        else:
            print("Invalid choice\n")
            continue

        break


if __name__ == "__main__":
    main()
