class CommonUI:
    @staticmethod
    def player_joined(nickname):
        if not nickname:
            raise ValueError("Nickname must not be empty")

        print(f"{nickname} joined the game\n")

    @staticmethod
    def player_left(nickname):
        if not nickname:
            raise ValueError("Nickname must not be empty")

        print(f"{nickname} left the game\n")

    @staticmethod
    def player_kicked(name):
        print(f"Player {name} was kicked from the server\n")

    @staticmethod
    def cli_start(type):
        print(f"Basic {type.lower()} command-line interpreter (type 'help' for help)")

    @staticmethod
    def show_players(players):
        if len(players) == 0:
            print("No players are currently connected")
        else:
            print("\nPlayers:")
            for name in players:
                print(f"- {name}")

        print()
