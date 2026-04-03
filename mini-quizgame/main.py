from server.game_server import GameServer
from client.game_client import GameClient
from utils.json_loader import JSONLoader

# temp
import socket
from common.protocol import send, recv


def host_game():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen()

    client, _ = server.accept()
    print(recv(client))


def join_game():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))

    send(client, {"type": "answer", "answer": 2})


def main():
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
