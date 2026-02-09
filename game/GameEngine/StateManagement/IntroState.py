from game.GameEngine.StateManagement.GameStateBase import GameStateBase
from game.GameEngine.StateManagement.BirthSceneState import BirthSceneState

class IntroState(GameStateBase):
    def __init__(self, terminal_controller, session, pygame):
        self.terminal_controller = terminal_controller
        self.session = session
        self._done = False
        self.pygame = pygame
        self.music = session.music
        self.music.play("terminal", volume=0.6)
    
    def handle_event(self,event):
        self.terminal_controller.event_handler(event)
    
    def update(self):
        self.terminal_controller.update()
        if self.session.get_flag("accepted_simulation"):
            self._done = True

    def draw(self, surface):
        #surface.fill((0,0,0))
        self.terminal_controller.draw(surface)

    def is_done(self): 
        return self._done
    
    def next_state(self):
        return BirthSceneState(self.terminal_controller, self.session,self.pygame)
