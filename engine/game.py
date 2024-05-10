import pygame
from pygame import Vector2 as vec2

from .map import Map
from .player import Player
from .light import LightSource
from .camera import Camera

class Game:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.__width = self.width // 2
        self.__height = self.height // 2
        self.game_is_running = True
        self.FPS = 60

        self.window = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.Surface((self.__width, self.__height))
        self.fps = pygame.time.Clock()

        self.maps = [
            Map("assets/maps/start_screen.csv", self.screen, self.screen.get_width() / 40),
            Map("assets/maps/default_map.csv", self.screen, self.screen.get_width() / 20),
            Map("assets/maps/map1.csv", self.screen, self.screen.get_width() / 20)
        ]
        self.current_map = self.maps[0]

        self.player = Player("assets/sprites/player.png", self.current_map.map_rect_width, self.screen)
        self.light = LightSource(self.screen, self.player.pos, (80, 0, 0), 1000)

        self.camera = Camera(self.screen, self.player, self.current_map)
        self.offset = vec2(0, 0)
        self.scroll = vec2
        self.k = 1 / 20
        
    def update(self):
        if self.current_map.start_game_enabled:
            self.current_map = self.maps[1]
        if self.current_map.map1_enabled:
            self.current_map = self.maps[2]
        fps_caption = f"FPS: {int(self.fps.get_fps())}"
        player_pos_caption = f"Player Pos: {int(self.player.pos.x)}, {int(self.player.pos.y)}"
        pygame.display.set_caption(f"{fps_caption} | {player_pos_caption}")
        self.screen.fill((5, 5, 5))

        # rects_in_vision = [rect for rect in self.current_map.map_rects if rect.colliderect(self.window.get_rect())]
        self.light.pos = self.player.pos
        # self.light.pos = vec2(self.screen.get_size())

        self.offset += self.k * (self.player.pos - 0.5 * vec2(self.window.get_rect().center) - self.offset)
        self.scroll = vec2(int(self.offset.x), int(self.offset.y))

        # self.light.show(rects_in_vision, self.scroll)
        self.light.show(self.current_map.nearby_rects, self.scroll)
        self.camera.update(self.player.pos)

        self.current_map.draw(self.scroll, self.player.pos, self)
        self.player.move(self.current_map)
        self.player.draw(self.scroll, self.current_map)

        self.window.blit(pygame.transform.scale2x(self.screen), (0, 0))
        pygame.display.update()
        self.fps.tick(self.FPS)

    def run(self):
        while self.game_is_running and not self.current_map.end_game_enabled:
            self.handle_key_events()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
            self.update()
        pygame.quit()
        quit()

    def handle_key_events(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_a]:
            self.player.vel += vec2(-self.player.speed, 0)
        if key[pygame.K_d]:
            self.player.vel += vec2(self.player.speed, 0)
        if key[pygame.K_SPACE] and self.player.standing_on_ground:
            self.player.jump()
        if key[pygame.K_ESCAPE] and self.current_map == self.maps[0]:
            self.game_is_running = False


