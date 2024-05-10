import csv
from typing import List

import pygame
from pygame import Vector2 as vec2

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path, scale=0.5):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(img_path)
        self.scaled_image = pygame.transform.scale(
            self.original_image,
            (
                int(self.original_image.get_width() * scale),
                int(self.original_image.get_height() * scale)
            )
        )
        self.rect = self.scaled_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Map:
    def __init__(self, path: str, surface: pygame.surface.Surface, size: float) -> None:
        self.path = path
        self.surface = surface
        self.map_rect_width = size
        self.map_tile_image = pygame.Surface((self.map_rect_width, self.map_rect_width))
        self.map_tile_image.fill((100, 100, 100))

        self.data = []
        self.light_pos = []
        with open(path, "r") as f:
            reader = csv.reader(f)
            for line in reader:
                self.data.append(line)

        self.start_game_rect = None
        self.end_game_rect = None
        self.map1_rect = None

        self.exit_group = pygame.sprite.Group()
        exit_gate = Exit(730, 0, 'assets/sprites/door.JPG')
        yippie = Exit(0, 0, 'assets/sprites/door.JPG')
        self.exit_group.add(exit_gate)
        self.exit_group.add(yippie)

        self.map_rects: List[pygame.Rect] = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == '2':
                    self.player_pos = self.map_rect_width * vec2(j, i)
                    self.offset = - self.player_pos + 0.5 * vec2(self.surface.get_size()) - 0.5 * vec2(self.map_rect_width, self.map_rect_width)
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == '3':
                    self.light_pos.append(vec2(
                        j * self.map_rect_width + self.offset.x,
                        i * self.map_rect_width + self.offset.y
                    ))
                if self.data[i][j] == '7':
                    self.map1_rect = pygame.Rect(
                        self.map_rect_width * vec2(j, i) + self.offset,
                        self.map_rect_width * vec2(1, 1)
                    )
                if self.data[i][j] == '8':
                    self.start_game_rect = pygame.Rect(
                        self.map_rect_width * vec2(j, i) + self.offset,
                        self.map_rect_width * vec2(1, 1)
                    )
                if self.data[i][j] == '9':
                    self.end_game_rect = pygame.Rect(
                        self.map_rect_width * vec2(j, i) + self.offset,
                        self.map_rect_width * vec2(1, 1)
                    )
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == '1':
                    self.map_rects.append(pygame.Rect((
                        j * self.map_rect_width + self.offset.x,
                        i * self.map_rect_width + self.offset.y,
                        self.map_rect_width,
                        self.map_rect_width
                    )))

        if self.start_game_rect:
            self.map_rects.append(self.start_game_rect)
        if self.end_game_rect:
            self.map_rects.append(self.end_game_rect)
        if self.map1_rect:
            self.map_rects.append(self.map1_rect)

        self.nearby_rects = []

        self.start_game_enabled = False
        self.end_game_enabled = False
        self.map1_enabled = False

    def draw(self, scroll, player_pos: vec2, game):
        self.nearby_rects.clear()
        for rect in self.map_rects:
            distance = (player_pos - vec2(rect.center)).magnitude_squared()
            if distance <= (self.surface.get_width() ** 2):
                self.nearby_rects.append(rect)
                self.surface.blit(self.map_tile_image, rect.move(-scroll))
        if self.start_game_rect:
            pygame.draw.rect(self.surface, (255, 0, 0), self.start_game_rect.move(-scroll))
        if self.end_game_rect:
            pygame.draw.rect(self.surface, (255, 0, 0), self.end_game_rect.move(-scroll))
        if self.map1_rect:
            pygame.draw.rect(self.surface, (255, 0, 0), self.map1_rect.move(-scroll))

        if game.current_map == game.maps[0]:
            for exit_gate in self.exit_group.sprites():
                exit_rect = exit_gate.rect.move(-scroll)
                self.surface.blit(exit_gate.scaled_image, exit_rect)
        else:
            # Clear the exit_group for other maps
            self.exit_group.empty()