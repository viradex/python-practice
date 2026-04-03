from dataclasses import dataclass


@dataclass
class Question:
    question: str
    choices: list[str]
    answer_index: int
