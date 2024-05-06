from .map import Map
from .player import Player
from .light import LightSource
from .camera import Camera

import pygame
from pygame import Vector2 as vec2
from .helper import run_typing_game

class Game:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.__width = self.width//2
        self.__height = self.height//2
        self.game_is_running = True
        self.FPS = 60

        self.window = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.Surface((self.__width, self.__height))
        self.fps = pygame.time.Clock()
        self.level=1

        self.maps = [
            Map("assets/maps/start_screen.csv", self.screen, self.screen.get_width() / 40),
            Map("assets/maps/map1.csv", self.screen, self.screen.get_width() / 20),
            Map("assets/maps/map2.csv", self.screen, self.screen.get_width() / 20),
            Map("assets/maps/map3.csv", self.screen, self.screen.get_width() / 20),
            Map("assets/maps/map4.csv", self.screen, self.screen.get_width() / 20),
            Map("assets/maps/map5.csv", self.screen, self.screen.get_width() / 20)
        ]
        self.current_map = self.maps[0]

        self.player = Player("assets/sprites/player.png", self.current_map.map_rect_width, self.screen)
        self.light = LightSource(self.screen, self.player.pos, (80, 0, 0), 1000)

        self.camera = Camera(self.screen, self.player, self.current_map)
        self.offset = vec2(0, 0)
        self.scroll = vec2
        self.k = 1 / 20
        self.is_mini_game_active = False

    def update(self):
        if self.current_map.start_game_enabled:
            self.current_map = self.maps[1]

        fps_caption = f"FPS: {int(self.fps.get_fps())}"
        player_pos_caption = f"Player Pos: {int(self.player.pos.x)}, {int(self.player.pos.y)}"
        pygame.display.set_caption(f"{fps_caption} | {player_pos_caption}")

        self.screen.fill((5, 5, 5))

        # rects_in_vision = [rect for rect in self.current_map.map_rects if rect.colliderect(self.window.get_rect())]
        self.light.pos = self.player.pos # RTX ENABLE (1/2)
        # self.light.pos = vec2(self.screen.get_size())

        self.offset += self.k * (self.player.pos - 0.5 * vec2(self.window.get_rect().center) - self.offset)
        self.scroll = vec2(int(self.offset.x), int(self.offset.y))

        # self.light.show(rects_in_vision, self.scroll)
        self.light.show(self.current_map.nearby_rects, self.scroll) # RTX ENABLE (2/2)
        self.camera.update(self.player.pos)

        self.current_map.draw(self.scroll, self.player.pos)
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
            
        exit_collision = pygame.sprite.spritecollide(self.player, self.current_map.exit_group, False)
        if exit_collision:
            self.level += 1  # Increment level
            if self.level > 5:
                self.level = 1  # Reset to level 1 if exceeds the number of maps
        
            self.current_map = self.reset_level(self.level)

        # Handle jump animation
        if key[pygame.K_SPACE] and self.player.standing_on_ground:
            self.player.jump()

        if key[pygame.K_f]:
            enemy_collision = pygame.sprite.spritecollide(self.player, self.current_map.get_blob_group(), False)
            if enemy_collision:
                typing_game_result = run_typing_game()
                if typing_game_result:
                    pass
                else:
                    pass


        if key[pygame.K_ESCAPE] and self.current_map == self.maps[0]:
            self.game_is_running = False

    def reset_level(self, level): ## investigate, probably not needed
        # Clear the current map data
        self.current_map.data.clear()
        self.current_map.map_rects.clear()
        self.current_map.blob_group.empty()
        self.current_map.exit_group.empty()
        
        # Ensure level stays within the valid range
        num_maps = len(self.maps)
        if level < 0:
            level = 0
        elif level >= num_maps:
            level = num_maps - 1
        
        self.current_map = self.maps[level]
        
        # Reset player position and other necessary data
        player_x, player_y = self.current_map.get_player_spawn_pos()
        self.player.reset(player_x, player_y)
        self.camera = Camera(self.screen, self.player, self.current_map)
        self.offset = vec2(0, 0)
        
        return self.current_map
