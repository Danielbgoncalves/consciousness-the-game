import pygame
from game.Mascot.Animation import Animation

class Mascot(pygame.sprite.Sprite):
    def __init__(self,memory_manager, personality_manager):
        super().__init__() 
        self.memory_manager = memory_manager
        self.personality_manager = personality_manager

        self.default_image = pygame.image.load("assets/mascote/mascote.png").convert_alpha()
        self.current_frame = self.default_image
        self.rect = self.current_frame.get_rect(topleft=(300, 300))

        self.animations = {
            "nasce": Animation("nasce",90, 130,1,60, pygame),
            "pisca": Animation("pisca",90, 130,0,30, pygame),
            "idle": Animation("idle",300, 300,0,5,pygame),
            "sorri": Animation("sorri",300, 300, 2,5, pygame),
            "assustado": Animation("assustado",300, 300, 2,5, pygame)
        }

        self.state = "idle"
        self.set_animation_callback("nasce", lambda:self.set_state("pisca"))
        self.frames_velocity = 60 # 60 ciclos pra mudar um frame
        self.actual_frame = 0
        self.count = 0
        self.repetition_count = 0

    def draw(self, surface):
        surface.blit(self.current_frame, self.rect)

    def set_position(self,x,y):
        self.rect = self.current_frame.get_rect(topleft=(x, y))
    
    def update(self):
        animation = self.animations[self.state]
        frames = animation.frames
        
        self.count += 1
        if self.count >= animation.velocity:
            self.count = 0
            self.actual_frame += 1

            if self.actual_frame >= len(frames):
                self.actual_frame = 0
                self.repetition_count += 1

                if animation.repeat_times != 0 and self.repetition_count >= animation.repeat_times:

                    if animation.on_finish:
                        animation.on_finish()
                    else:
                        self.set_state("idle")
                        return
        
        self.current_frame = frames[self.actual_frame]
    
    def set_state(self, new_state):
        if new_state != self.state:
            print(f"mudou pra {new_state}")
            self.state = new_state
            self.actual_frame = 0
            self.count = 0
            self.repetition_count = 0
    
    def set_animation_callback(self, animation_name, callback):
        if animation_name in self.animations:
            self.animations[animation_name].on_finish = callback