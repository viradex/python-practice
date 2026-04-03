from server.game_state import GameState


class GameServer:
    def __init__(self, host, port, questions):
        self.host = host
        self.port = port
        self.questions = questions
        self.clients = []
        self.state = GameState()

    def start(self):
        pass

    def accept_clients(self):
        pass

    def broadcast(self, message):
        pass

    def run_game(self):
        pass

    def ask_question(self, question):
        pass

    def collect_answers(self):
        pass

    def calculate_scores(self):
        pass
