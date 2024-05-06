from .player import Player
from .map import Map

import pygame

class Camera:
    def __init__(self, surface: pygame.Surface, player: Player, map: Map) -> None:
        self.player = player
        self.map = map
        self.surface = surface

    def update(self, player_pos):
        # self.pos = pygame.Vector2(self.surface.get_rect().center) - player_pos
        pass
