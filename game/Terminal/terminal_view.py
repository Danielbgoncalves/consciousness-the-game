from game.Terminal.message_type import Message, MessageType
from game.util import cores
import time

class TerminalView:
    def __init__(self, x,width, height, pygame):
        self.x = x
        self.width = width
        self.height = height
        self.lines = []
        self.input_text = ""
        self.pygame = pygame

        self.player_can_type = True
        self.scroll_offset = 0  # Deslocamento do scroll

        self.style_map = {
            MessageType.JOGADOR: {
                "FONT": self.pygame.font.SysFont("Courier New", 18, italic=True),
                "COLOR": (0, 255, 0)
            },
            MessageType.MASCOTE: {
                "FONT": self.pygame.font.SysFont("Courier New", 18, bold=True),
                "COLOR": (190, 85, 190)
            },
            MessageType.SIMULACAO: {
                "FONT": self.pygame.font.SysFont("Courier New", 18, ),
                "COLOR": (200, 200, 200)
            },
             MessageType.MULT_CHOICE: {
                "FONT": self.pygame.font.SysFont("Courier New", 18),
                "COLOR": (255, 255, 0)
            }

        }

    def set_player_can_type(self, is_able):
        self.player_can_type = is_able
    
    def get_max_lines(self):
        return (self.height - 40) // 22  # 22 é a altura de cada linha + espaçamento

    def add_line(self, text):
        if  isinstance(text, Message):
            msg_type = text.type
            font = self.style_map.get(msg_type)["FONT"]

            lines = self.wrap_text(text.text, font,self.width - 15 )
            for line in lines:
                self.lines.append(Message(line, msg_type))
        else:
            self.lines.append(text)  

    
    def update_input_text(self, text):
        self.input_text = text
    
    def draw(self, surface):
        self.pygame.draw.rect(surface, cores["TERMINAL_COLOR"], (self.x, 0, self.width, self.height))
        y = 10

        max_lines = self.get_max_lines()
        start = max(0, len(self.lines) - max_lines - self.scroll_offset)
        end = start + max_lines

        visible_lines = self.lines[start:end]

        for line in visible_lines:
            if isinstance(line, Message):
                style = self.style_map.get(line.type, self.style_map[MessageType.SIMULACAO])
                font = style["FONT"]
                color = style["COLOR"]
                rendered = font.render(line.text, True, color)
            else:
                font = self.pygame.font.SysFont("Courier New", 18)
                color = (255, 255, 255)
                rendered = font.render(line, True, color)

            surface.blit(rendered, (self.x + 10, y))
            y += 22

        if self.player_can_type:
            cursor = "_" if int(time.time() * 2) % 2 == 0 else ""
            font = self.pygame.font.SysFont("Courier New", 18)
            input_render = font.render("> " + self.input_text + cursor, True, cores["TERMINAL_TXT"])
            surface.blit(input_render, (self.x + 10, y))


    def wrap_text(self,text,font, width):
        lines = []
        words = text.split(" ")
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line)

        return lines