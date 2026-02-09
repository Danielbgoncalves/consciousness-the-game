from enum import Enum

class MessageType(Enum):
    JOGADOR = 1
    MASCOTE = 2
    SIMULACAO = 3
    MULT_CHOICE = 4

class Message:
    def __init__(self, text: str, msg_type: MessageType):
        self.text = text
        self.type = msg_type
