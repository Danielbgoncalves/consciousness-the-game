from game.GameEngine.StateManagement.GameStateBase import GameStateBase
from game.GameEngine.StateManagement.InteractiveMapState import InteractiveMapState

class BirthSceneState(GameStateBase):
    def __init__(self, terminal_controller,session,pygame):
        self.terminal_controller = terminal_controller
        self.session = session
        self.mascot = self.session.mascot
        self.music = session.music

        self.egg_clicked = False
        self.born_mascot = False
        self._done = False
        self.pygame = pygame
        self.background_image = self.pygame.image.load("assets/garden.png").convert_alpha()
        self.background_image_rect = self.background_image.get_rect(topleft=(0,0))

        self.mascot.set_state("nasce")
        self.music.play("nasce", volume=0.3)
        

    def handle_event(self, event):
        self.terminal_controller.event_handler(event)

        if event.type == self.pygame.MOUSEBUTTONDOWN:
            if not self.egg_clicked:
                # if na area do ovo o clique
                self.egg_clicked = True
    
    def update(self):
        self.mascot.update()
        self.terminal_controller.update()

        if self.egg_clicked:
            # TODO: animação de nascimento
            pass
        
        if self.mascot:
            # animação básica dele
            pass

        # em algum momento self._done = True
        
    def draw(self, surface):
       
        surface.blit(self.background_image, self.background_image_rect)
        self.mascot.draw(surface)
        self.terminal_controller.draw(surface)

        # desenhar o jardim (imagem carregada)

        if not self.egg_clicked:
            # desenha ovo
            pass
        else:
            # nao desenha ovo e desenha personagem
            pass
    
    def is_done(self):
        return self._done
    
    def next_state(self):
        return InteractiveMapState(self.terminal_controller, self.session, self.pygame)
    
