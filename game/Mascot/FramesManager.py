class FramesManager():
    def __init__(self,pygame):
        self.pygame = pygame

    def get_frames(self,humor ,frame_w, frame_h):
        path = f"assets/mascote/{humor}.png"
        spritesheet = self.pygame.image.load(path).convert_alpha()
        return self.spritsheet_split(spritesheet, frame_w, frame_h)

    def spritsheet_split(self, spritesheet, width, heigth):
        frames = []

        sheet_w, sheet_h = spritesheet.get_size() 
        for y in range(0, sheet_h, heigth):
            for x in range(0, sheet_w, width):
                frame = spritesheet.subsurface(self.pygame.Rect(x, y, width, heigth))
                frames.append(frame)
        
        return frames