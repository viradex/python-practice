import ipaddress
from common.common_ui import CommonUI


class ClientUI(CommonUI):
    @staticmethod
    def join_server(host, port):
        print(f"Joined server on {host} on port {port}\n")

    @staticmethod
    def get_ip_address(default="127.0.0.1"):
        while True:
            ip = input(f"Enter IP address (or blank for {default}): ")

            if not ip:
                ip = default

            try:
                ipaddress.ip_address(ip)
                return ip
            except ValueError:
                print("Invalid address\n")

    @staticmethod
    def get_nickname():
        while True:
            nickname = input("Enter nickname: ").strip()

            if not nickname:
                print("The nickname must not be empty\n")
            else:
                break

        return nickname

    @staticmethod
    def connection_lost(reason):
        if not reason:
            reason = "<no reason provided>"

        print(f"Connection Lost\nReason: {reason}")

    @staticmethod
    def parse_command(cmd):
        parts = cmd.split()
        command = parts[0]

        if command == "help":
            return ("help", None)

        elif command == "list":
            return ("list", None)

        elif command == "quit":
            return ("quit", None)

        else:
            return ("invalid", None)

    @staticmethod
    def show_help():
        help_messages = {
            "list": "List all nicknames of players currently on the server",
            "quit": "Disconnect from the server",
            "help": "Show this menu",
        }

        for help_cmd in help_messages:
            print(f"{help_cmd} - {help_messages[help_cmd]}")

        print()
