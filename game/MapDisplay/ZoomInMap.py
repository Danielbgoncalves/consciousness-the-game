from game.MapDisplay.BaseSceneMap import BaseSceneMap 
from game.util import screen_config



class ZoomInMap(BaseSceneMap):
    def __init__(self, pygame, building_id, mannager):
        path = f"assets/buildings_in/b{building_id}.png"
        self.map_img = pygame.image.load(path).convert_alpha()
        self.map_rect = self.map_img.get_rect()
        self.map_rect.topleft = (0, screen_config["height"] / 2 - self.map_rect.height / 2)

        '''path2 = f"assets/mascote/mascote.png"
        self.map_img2 = pygame.image.load(path2).convert_alpha()
        self.map_rect2 = self.map_img2.get_rect()
        self.map_rect2.topleft = (0, screen_config["height"] / 2 - self.map_rect2.height / 2)'''

        self.mannager = mannager
        self.pygame = pygame
        self.buildings = building_id
    
    def draw(self, surface):
        surface.blit(self.map_img, self.map_rect)
        surface.blit(self.map_img2, self.map_rect2)

    def update(self, events):
        for event in events:
            if event.type == self.pygame.MOUSEBUTTONDOWN:
                self.mannager.change_to_general_scene()

