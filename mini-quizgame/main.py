from server.game_server import GameServer
from client.game_client import GameClient
from utils.json_loader import JSONLoader


def host_game():
    pass


def join_game():
    pass


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
