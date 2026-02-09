from game.GameEngine.StateManagement.InteractiveScenesManager import SceneManager
from game.GameEngine.StateManagement.GameStateBase import GameStateBase
from game.MapDisplay.ZoomOutMap import ZoomOutMap
from game.util import screen_config
from game import buildings_loader

class InteractiveMapState(GameStateBase):
    def __init__(self, terminal_controller, session, pygame):
        self.terminal_controller = terminal_controller
        self.session = session
        self.pygame = pygame
        
        # cria o gerenciador de cenas
        self.scene_manager = SceneManager(None)

        # cria o mapa com zoom out
        zoomout_map = ZoomOutMap(
            pygame=pygame,
            image_path="assets/general_map4.png",
            scene_manager=self.scene_manager,
            position=(-80, screen_config["height"] // 2 - 400)
        )

        buildings = buildings_loader.load()
        zoomout_map.add_building(buildings)
        self.scene_manager.set_general_scene(zoomout_map)

    
    def handle_event(self, event):
        self.terminal_controller.event_handler(event)
        self.scene_manager.update(event)

    def update(self):
        pass

    def draw(self,surface):
        self.terminal_controller.draw(surface)
        self.scene_manager.draw(surface)
    
    def is_done(self):
        return False
    
    def next_state(self):
        return self #sem outros estados por enquanto
