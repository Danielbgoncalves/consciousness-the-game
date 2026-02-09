from abc import ABC, abstractmethod

class BaseSceneMap(ABC):
    '''
        def __init__(self, pygame,surface, path):
            self.map_img = pygame.image.load(path).convert_alpha()
            self.surface = surface
            self.position = (0,0)
    '''
    @abstractmethod
    def draw(self):
        pass
        #self.surface.blit(self.map_img, self.position)

    @abstractmethod
    def update(self):
        pass
