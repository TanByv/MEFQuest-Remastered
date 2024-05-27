import pygame
from pygame import Vector2 as vec2

from .map import Map
from .player import Player
from .light import LightSource
from .minigame import MiniGame
from .elevator_minigame import run_game
from pygame import mixer

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
        self.k = 1 / 5  # camera sway co-efficient (default: 1/20)
        
        pygame.mixer.init()
        self.music = pygame.mixer.music.load("assets/sounds/music.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set volume to 50%


    def update(self):
        if self.current_map.start_game_enabled:
            self.current_map = self.maps[1]
        if self.current_map.map1_enabled:
            self.current_map = self.maps[2]
            xdtest = True
            while(xdtest):
                self.player.rect.topleft = (14, 210)  
                xdtest = False
        fps_caption = f"FPS: {int(self.fps.get_fps())}"
        player_pos_caption = f"Player Pos: {int(self.player.pos.x)}, {int(self.player.pos.y)}"
        pygame.display.set_caption(f"{fps_caption} | {player_pos_caption}")
        self.screen.fill((5, 5, 5))

        self.light.pos = self.player.pos

        self.offset += self.k * (self.player.pos - 0.5 * vec2(self.window.get_rect().center) - self.offset)
        self.scroll = vec2(int(self.offset.x), int(self.offset.y - 75))  # set camera offset here

        self.light.show(self.current_map.nearby_rects, self.scroll)

        self.current_map.draw(self.scroll, self.player.pos, self)
        self.player.move(self.current_map)
        self.player.draw(self.scroll, self.current_map, self.screen)

        self.window.blit(pygame.transform.scale2x(self.screen), (0, 0))
        pygame.display.update()
        self.fps.tick(self.FPS)

    def run(self):
        pygame.mixer.music.play(-1) 

        while self.game_is_running and not self.current_map.end_game_enabled:
            self.handle_key_events()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
            self.update()
        pygame.quit()
        quit()

    def start_mini_game(self, player_sprite, csv_filename, given_damage, taken_damage, set_time):
        # Save current dimensions
        current_dimensions = self.window.get_size()

        # Initialize and run the MiniGame, capturing the result
        mini_game = MiniGame(player_sprite, csv_filename, given_damage, taken_damage, set_time)

        # Restore main game dimensions after minigame ends
        self.window = pygame.display.set_mode(current_dimensions)

        return mini_game.result()
        
        
    def change_background(self, background_image_path):
        self.current_map.background_image = pygame.image.load(background_image_path).convert_alpha()
        self.current_map.background_width = self.current_map.background_image.get_rect().width
        self.current_map.background_height = self.current_map.background_image.get_rect().height
        self.current_map.background_image = pygame.transform.scale(
            self.current_map.background_image,
            (self.current_map.background_width, self.screen.get_height())
        )

    def run_mini_game(self):

        current_dimensions = self.window.get_size()
        score = run_game()
        self.window = pygame.display.set_mode(current_dimensions)
        return score

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
                        self.result = self.start_mini_game("guard", "guardian", 20, 15, 20)
                        if(self.result):
                                self.player.rect.topleft = (-160, 3800)
                        else:
                                self.player.rect.topleft = (14, 210)                           
                    elif x.type == "kantin":
                        self.result = self.start_mini_game("kantinci", "kantin", 20, 15, 20)
                        if(self.result):
                                self.player.rect.topleft = (-160, 3800)
                        else:
                                self.player.rect.topleft = (14, 210)                           
                    elif x.type == "ilker":
                        self.result = self.start_mini_game("ilker", "ilkay", 20, 15, 20)
                        if(self.result):
                                self.player.rect.topleft = (-160, 3800)
                        else:
                                self.player.rect.topleft = (20, 965)
                    elif x.type == "student":
                        self.result = self.start_mini_game("students", "prepstudent", 20, 15, 20)
                        if(self.result):
                                self.player.rect.topleft = (-160, 3800)
                        else:
                                self.player.rect.topleft = (20, 965)
                    elif x.type == "ogrenciisleri":
                        self.result = self.start_mini_game("ogrenciisleri", "ogrenciisleri", 20, 15, 20)
                        if(self.result):
                                self.player.rect.topleft = (-160, 3800)
                        else:
                                self.player.rect.topleft = (-178, 2210)
                    elif x.type == "ilber":
                        self.result = self.start_mini_game("kutuphaneci", "kutuphane", 20, 15, 20)
                        if(self.result):
                                self.player.rect.topleft = (-160, 3800)
                        else:
                                self.player.rect.topleft = (-58, 3045)
                    elif x.type == "erhan":
                        self.result = self.start_mini_game("erhan", "erkut", 20, 15, 20)
                        if(self.result):
                                self.player.rect.topleft = (-160, 3800)
                        else:
                                self.player.rect.topleft = (-196, 4500)
                    elif x.type == "rektor":
                        self.result = self.start_mini_game("rektor", "rektor", 20, 15, 20)
                        if(self.result):
                                self.player.rect.topleft = (-160, 3800)
                        else:
                                self.player.rect.topleft = (14, 210)
                    elif x.type == "brokenelevator":
                        if self.run_mini_game():
                            self.player.rect.topleft = (-196, 4500)
                            self.change_background("assets/sprites/glass.png")
                        else:
                            self.player.rect.topleft = (-160, 3800)
                    elif x.type == "door0":
                        self.player.rect.topleft = (20, 965)
                    elif x.type == "door1":
                        self.player.rect.topleft = (-178, 2210)
                    elif x.type == "door2":
                        self.player.rect.topleft = (-58, 3045)
                        self.change_background("assets/sprites/ahsap.png")
                    elif x.type == "door3":
                        self.player.rect.topleft = (-160, 3800)

                    #print(self.result)
