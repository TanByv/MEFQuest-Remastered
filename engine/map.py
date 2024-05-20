import csv
from typing import List

import pygame
from pygame import Vector2 as vec2

import math

class Spriteee(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path, scale=0.5, type="default"):
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
        self.type = type
        
class Map:
    def __init__(self, path: str, surface: pygame.surface.Surface, size: float) -> None:
        self.background_image = pygame.image.load("assets/sprites/jetpack.png").convert_alpha()
        self.background_width = self.background_image.get_rect().width
        self.background_height = self.background_image.get_rect().height
        # Scale the background image vertically to fit the game window
        self.background_image = pygame.transform.scale(
            self.background_image,
            (self.background_width, surface.get_height())
        )
        self.tiles = math.ceil(self.background_width / surface.get_width()) + 1
        self.scroll = 0

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
        
        #startscreen
        self.startScreen_group = pygame.sprite.Group()
        exit_gate = Spriteee(-200, 50, 'assets/sprites/door.JPG', type="doorTest")
        self.startScreen_group.add(exit_gate)

        #map1
        self.map1 = pygame.sprite.Group()
        guard = Spriteee(830, 30, 'assets/sprites/guard.png', type="guard")
        self.map1.add(guard)
        #turnike = Spriteee(200, -15, 'assets/sprites/turnike.JPG', guard)
        kantin = Spriteee(2000, -150, 'assets/sprites/kantin.png', type="kantin")
        self.map1.add(kantin)
        kantinci = Spriteee(1800, 10, 'assets/sprites/kantinci.png', type="kantin")
        self.map1.add(kantinci)
        #xd
        door0 = Spriteee(3400, 70, 'assets/sprites/door.png', type="door0")
        self.map1.add(door0)
        #ilker
        ilker = Spriteee(500, 820, 'assets/sprites/ilker.png', type="iker")
        self.map1.add(ilker)
        #classroom
        classroom = Spriteee(2000, 805, 'assets/sprites/classroom.PNG', type="classroom")
        self.map1.add(classroom)
        #Student
        student = Spriteee(1500, 715, 'assets/sprites/students.PNG', type="student")
        self.map1.add(student)
        #door1
        door1 = Spriteee(3400, 830, 'assets/sprites/door.png', type="door1")
        self.map1.add(door1)
        #door2
        door2 = Spriteee(3400, 2150, 'assets/sprites/door.png', type="door2")
        self.map1.add(door2)
        #ilber
        ilber = Spriteee(1900, 2845, 'assets/sprites/kutuphaneci.png', type="ilber")
        self.map1.add(ilber)
        #book
        book = Spriteee(100, 3532, 'assets/sprites/bok.png', type="book")
        self.map1.add(book)
        #library
        library = Spriteee(2500, 2845, 'assets/sprites/kütüphane.png', type="library")
        self.map1.add(library)
        

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
        if self.path == "assets/maps/map1.csv":
            # Calculate the background offset based on the player's position
            background_offset_x = (player_pos.x - self.player_pos.x) % self.background_width
            # Draw scrolling background
            for i in range(0, self.tiles):
                self.surface.blit(self.background_image, (i * self.background_width - background_offset_x, 0))


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
            for exit_gate in self.startScreen_group.sprites():
                exit_rect = exit_gate.rect.move(-scroll)
                self.surface.blit(exit_gate.scaled_image, exit_rect)
        elif game.current_map == game.maps[2]:
            self.startScreen_group.empty()
            for exit_gate in self.map1.sprites():
                exit_rect = exit_gate.rect.move(-scroll)
                self.surface.blit(exit_gate.scaled_image, exit_rect)
        else:
            # Clear the exit_group for other maps
            self.startScreen_group.empty()