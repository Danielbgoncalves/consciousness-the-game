from game.Mascot.FramesManager import FramesManager

class Animation:
    def __init__(self, name,frames_width,frames_heidth,repeat_times, velocity, pygame, on_finish=None):
        '''
        frames: lista de frames (pygame.Surface)
        repeate_times:
            0 -> infinitas vezes
            N -> N vezes
        '''
        frames_manager = FramesManager(pygame)
        self.frames = frames_manager.get_frames(name,frames_width,frames_heidth)
        self.repeat_times = repeat_times
        self.on_finish = on_finish
        self.velocity = velocity
