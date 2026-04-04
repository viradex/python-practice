from enum import Enum


class MessageType(str, Enum):
    """Defines all valid message types that can be sent/received between the client and the server."""

    JOIN = "join"
    PIN = "pin"
    PLAYER_LIST = "player_list"
    START = "start"

    QUESTION = "question"
    ANSWER = "answer"
    RESULT = "result"
    END = "end"
