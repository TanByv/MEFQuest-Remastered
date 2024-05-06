import pygame
from .typing_minigame import main as typing_game

def run_typing_game():
    # Pause the game
    pygame.display.iconify()

    # Run the mini-game
    typing_game_result = typing_game()

    # Recreate the window surface
    window_surface = pygame.display.set_mode((1280, 920))

    return typing_game_result

