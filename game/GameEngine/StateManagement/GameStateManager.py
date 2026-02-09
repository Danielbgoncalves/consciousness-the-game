class GameStateManager:
    def __init__(self, initial_state):
        self.current_state = initial_state

    def update(self):
        self.current_state.update()
        if self.current_state.is_done():
            self.current_state = self.current_state.next_state()

    def handle_event(self, event):
        self.current_state.handle_event(event)

    def draw(self, surface):
        self.current_state.draw(surface)
