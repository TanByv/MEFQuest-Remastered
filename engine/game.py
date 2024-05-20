import pygame
from pygame import Vector2 as vec2

from .map import Map
from .player import Player
from .light import LightSource
from .minigame import MiniGame

class Game:
    def __init__(self):
        self.width = 1600
        self.height = 900
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

        self.offset = vec2(0, 0)
        self.scroll = vec2
        self.k = 1 / 5 # camera sway co-efficient (default: 1/20)
        
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
        self.scroll = vec2(int(self.offset.x), int(self.offset.y - 75)) # set camera offset here

        # self.light.show(rects_in_vision, self.scroll)
        self.light.show(self.current_map.nearby_rects, self.scroll)

        self.current_map.draw(self.scroll, self.player.pos, self)
        self.player.move(self.current_map)
        self.player.draw(self.scroll, self.current_map, self.screen)

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

    def start_mini_game(self, player_sprite, csv_filename):
        self.mini_game = MiniGame(player_sprite, csv_filename)

    def handle_key_events(self):
        key = pygame.key.get_pressed()

       # Reset animation if no movement keys are pressed
        if not key[pygame.K_a] and not key[pygame.K_d]:
            self.player.vel.x = 0
            self.player.update_animation()

        # Handle other key events
        if key[pygame.K_a]:
            self.player.vel += vec2(-self.player.speed, 0)
            self.player.direction = -1  # Set direction to left
            self.player.counter += 1  # Increment animation counter
        elif key[pygame.K_d]:
            self.player.vel += vec2(self.player.speed, 0)
            self.player.direction = 1  # Set direction to right
            self.player.counter += 1  # Increment animation counter

        # Update animation if enough frames have passed
        if self.player.counter > self.player.walk_cooldown:
            self.player.update_animation()
            
        # Handle jump animation
        if key[pygame.K_SPACE] and self.player.standing_on_ground:
            self.player.jump()

        if key[pygame.K_ESCAPE] and self.current_map == self.maps[0]:
            self.game_is_running = False
            
        if key[pygame.K_f]:
            for x in self.current_map.map1:
                enemy_coll = pygame.sprite.collide_rect(self.player, x)
                if enemy_coll:
                    if x.type == "guard":
                        self.start_mini_game("guard", "guardian")
                    elif x.type == "kantin":
                        self.start_mini_game("kantinci", "kantin")
                    elif x.type == "door0":
                        self.player.rect.topleft = (20, 965)
                    elif x.type == "door1":
                        self.player.rect.topleft = (-178, 2210)
                    elif x.type == "door2":
                        self.player.rect.topleft = (-58, 3045)
