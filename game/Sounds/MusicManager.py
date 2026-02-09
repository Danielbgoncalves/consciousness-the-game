class MusicManager:
    def __init__(self, pygame):
        pygame.mixer.init()
        self.pygame = pygame
        self.music = {
            "terminal": "assets/sounds/terminal_theme.mp3",
            "nasce": "assets/sounds/mascote_nasce.mp3"
        }

    def play(self, music_name, volume=0.5, loop=True):
        music = self.pygame.mixer.music
        if music: music.stop()

        music.load(self.music[music_name])
        music.set_volume(volume)
        music.play(-1 if loop else 0)


    def stop(self):
        self.pygame.mixer.music.stop()

    