from game.Terminal.message_type import MessageType, Message
import re

class TerminalController:
    def __init__(self, terminal_view):
        self.view = terminal_view
        self.input_text = ""
        self.on_sent_message = None
        self.pygame = self.view.pygame

        self.pending_messages = []
        self.last_msg_time = 0
        self.player_can_type = True

        self.on_finish_slw_msg = None

    def set_player_can_type(self, is_able):
        self.player_can_type = is_able
        self.view.set_player_can_type(is_able)

    def event_handler(self, event): 
        if event.type == self.pygame.MOUSEBUTTONDOWN:
            if event.button == 5:  # Scroll pra cima
                self.view.scroll_offset = max(0, self.view.scroll_offset - 1)
            if event.button == 4:  # Scroll pra baixo
                max_offset = max(0, len(self.view.lines) - self.view.get_max_lines())
                self.view.scroll_offset = min(max_offset, self.view.scroll_offset + 1)

        # Se não pode digitar ignora tudo
        if not self.player_can_type:
            return

        if event.type == self.pygame.KEYDOWN:
            if event.key == self.pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == self.pygame.K_RETURN:
                if self.input_text.strip() == "":
                    self.send_message("Entrada Inválida", MessageType.SIMULACAO)
                else:
                    self.send_message(self.input_text, MessageType.JOGADOR)
                    if self.on_sent_message: # se o callback foi definido
                        self.on_sent_message(self.input_text) # vai pro StoryManager
                self.input_text = ""
            else:
                self.input_text += event.unicode
            self.update_input_text(self.input_text)


    def send_message(self, message, auth):
            msg = Message(message, auth)
            self.view.add_line(msg)
    
    def send_message_slowly(self, message, auth, delay=1000, on_finish=None):
        self.set_player_can_type(False) 

        frases = re.split(r'(?<=[!?])\s+', message)
        current_time = self.pygame.time.get_ticks()
        for i, frase in enumerate(frases):
            self.pending_messages.append((current_time + i * delay, frase, auth))

        self.on_finish_slw_msg = on_finish
    
    def update(self):
        now = self.pygame.time.get_ticks()
        while self.pending_messages and now >= self.pending_messages[0][0]:
            _, frase, auth = self.pending_messages.pop(0)
            self.send_message(frase, auth)

        if not self.pending_messages:
            self.set_player_can_type(True)

            if self.on_finish_slw_msg:
                callback = self.on_finish_slw_msg
                self.on_finish_slw_msg = None
                callback()

    def draw(self, surface):
        self.view.draw(surface)

    def update_input_text(self, text):
        self.view.update_input_text(text)

    def show_options(self, options):
        for i, option in enumerate(options, start=1):
            self.send_message(f"{i}_ {option}", MessageType.MULT_CHOICE)
