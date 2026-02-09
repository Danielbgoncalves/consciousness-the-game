class GameSession:
    def __init__(self, mascot, music_manager):
        self.mascot = mascot
        self.music = music_manager
        self.flags = {}

    def set_flag(self, key, value=True):
        self.flags[key] = value

    def get_flag(self, keya):
        return self.flags.get(keya,False) # False é o valor padrão caso não encontre essa chave no dicionário