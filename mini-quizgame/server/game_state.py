class GameState:
    def __init__(self):
        self.players = {}  # name -> score
        self.answers = {}  # name -> answer

        self.current_question = None

    def add_player(self, name):
        self.players[name] = 0

    def submit_answer(self, name, answer):
        self.answers[name] = answer

    def all_answered(self):
        pass

    def clear_answers(self):
        self.answers.clear()
