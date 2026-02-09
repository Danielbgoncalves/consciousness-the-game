class SceneManager:
    def __init__(self, innitial_scene):
        self.actual_scene = innitial_scene
        self.general_scene = innitial_scene

    def set_general_scene(self, scene):
        self.actual_scene = scene
        self.general_scene = scene
        
    def change_scene(self, new_scene):
        self.actual_scene = new_scene

    def change_to_general_scene(self):
        self.actual_scene = self.general_scene
    
    def draw(self, surface):
        self.actual_scene.draw(surface)

    def update(self, event):
        self.actual_scene.update(event)
    