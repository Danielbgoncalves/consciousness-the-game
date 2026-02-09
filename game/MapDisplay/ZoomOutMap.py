from game.MapDisplay.BaseSceneMap import BaseSceneMap
from game.MapDisplay.ZoomInMap import ZoomInMap 

class ZoomOutMap(BaseSceneMap):
    def __init__(self, pygame, path, mannager, position=(0,0)):
        self.map_img = pygame.image.load(path).convert_alpha()
        #self.map_img = pygame.transform.scale_by(self.map_img, 1.2)
        self.position = position
        self.pygame = pygame
        self.mannager = mannager
        self.buildings = []
    
    def draw(self, surface):
        surface.blit(self.map_img, self.position)
        for b in self.buildings:
            b.draw(surface)

    def update(self, events):
        for event in events:
            if event.type == self.pygame.MOUSEBUTTONDOWN:
                for b in self.buildings:
                    if b.rect.collidepoint(event.pos):
                        new_scene = ZoomInMap(self.pygame, b.id, self.mannager)
                        self.mannager.change_scene(new_scene)

    def add_building(self, buildings):
        for b in buildings:
            self.buildings.append(b)