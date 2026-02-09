class Building:
    def __init__(self, b_id, x, y, image):
        self.id = b_id
        self.image = image # nao receber o path mas a img mesmo
        self.rect = self.image.get_rect(topleft=(x,y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)