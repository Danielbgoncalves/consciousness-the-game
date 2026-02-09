import pygame, sys, json

from game.Terminal.terminal_controller import TerminalController
from game.Terminal.terminal_view import TerminalView
from game.util import screen_config, map_config, terminal_config, cores
from game.GameEngine.StoryManager import StoryManager
from game.GameEngine.GameSession import GameSession
from game.GameEngine.StateManagement.GameStateManager import GameStateManager
from game.GameEngine.StateManagement.IntroState import IntroState
from game.Mascot.Mascot import Mascot
from game.Mascot.MemoryManager import MemoryManager
from game.Mascot.PersonalityManager import PersonalityManager
from game.GameEngine.Gemini.AIAssistant import AIAssistant
from game.GameEngine.InputManager import InputManager
from game.Sounds.MusicManager import MusicManager

pygame.init()

# Configurações iniciais
screen = pygame.display.set_mode(screen_config["size"])
title = "Consciência - protótipo"
clock = pygame.time.Clock()

# JSON com a história -> dicionário do python
with open("game/gameEngine/story_map.json", "r", encoding="utf-8") as f:
    story_data = json.load(f)

# Terminal
terminal_view = TerminalView(map_config["width"], terminal_config["width"], screen_config["height"], pygame)
terminal_controller = TerminalController(terminal_view)

# gerentes da mente do mascote
memory_manager = MemoryManager()
personality_manager = PersonalityManager()

# Mascote
mascot = Mascot(memory_manager, personality_manager)

# Música
music_manager = MusicManager(pygame)

# GameSession
game_session = GameSession(mascot, music_manager)

# Define conexão com o Gemini
ai_assistant = AIAssistant(personality_manager.personality)

# Gerenciador do input
input_manager = InputManager(ai_assistant)

# StoryManager
story_manager = StoryManager(story_data, terminal_controller, game_session, ai_assistant, input_manager)

# Game State Manager
initial_state = IntroState(terminal_controller,game_session, pygame)
game_state_manager = GameStateManager(initial_state)


in_game = True
while in_game:
    clock.tick(60)

    # Itera por cada evento de cada frame
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            in_game = False
        
        game_state_manager.handle_event(event)
    
    # MAP
    pygame.draw.rect(screen, cores["MAP_COLOR"], (0,0,map_config["width"],screen_config["height"]))
    
    game_state_manager.update()
    game_state_manager.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()

'''
    TODO: precisa dar uma organizada no JSON. 
    ta ficando intratável a forma como ele cresce e ta difícil enetender qual nó chama qual
    Mlehorar os nomes dos nós ajuda um pouco

    Ideia: no final da fase 1 podia gerar um relatório da personalidade do mascote, escrever de forma bem imersiva e cativante, ia er legal

'''