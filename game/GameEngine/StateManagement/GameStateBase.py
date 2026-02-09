class GameStateBase:
    def handle_event(self, event): pass
    def update(self): pass
    def draw(self, surface): pass
    def is_done(self): pass
    def next_state(self): pass