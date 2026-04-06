class GameState:
    def __init__(self):
        self.players = {}  # name -> score
        self.answers = {}  # name -> answer

        self.current_question = None

    def add_player(self, name):
        self.players[name] = 0

    def submit_answer(self, name, answer):
        if name not in self.answers:
            self.answers[name] = answer

    def all_answered(self):
        return len(self.answers) >= len(self.players)

    def clear_answers(self):
        self.answers.clear()

    def calculate_scores(self):
        correct = self.current_question["answer_index"]

        for player, answer in self.answers.items():
            if answer == correct:
                self.players[player] += 1
