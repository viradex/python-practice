from common.common_ui import CommonUI


class ServerUI(CommonUI):
    @staticmethod
    def start_server(host, port):
        print(f"Started server, listening on {host} on port {port}\n")

    @staticmethod
    def client_connected(ip, port):
        print(f"Client joined (IP {ip}:{port})")

    @staticmethod
    def server_shutdown():
        print("Server has been shut down\n")

    @staticmethod
    def parse_command(cmd):
        parts = cmd.split()
        command = parts[0]

        if command == "help":
            return ("help", None)

        elif command == "start":
            return ("start", None)

        elif command == "list":
            return ("list", None)

        elif command == "kick":
            if len(parts) < 2:
                return ("error", "Name must be provided")
            return ("kick", parts[1])

        elif command == "stop":
            return ("stop", None)

        else:
            return ("invalid", None)

    @staticmethod
    def show_help():
        help_messages = {
            "start": "Start the game",
            "list": "List all nicknames of players currently on the server",
            "kick <name>": "Kick the specified player from the server",
            "stop": "Shut down the server",
            "help": "Show this menu",
        }

        for help_cmd in help_messages:
            print(f"{help_cmd} - {help_messages[help_cmd]}")

        print()
