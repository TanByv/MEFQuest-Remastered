import pygame
from .map import Map

class Player:
    def __init__(self, img_path: str, size: float, surface: pygame.Surface) -> None:
        self.index = 0
        self.counter = 0
        self.walk_cooldown = 5

        # Animation images
        self.images_right = []
        self.images_left = []
        for num in range(1, 5):
            img_right = pygame.image.load(f'assets/sprites/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]  # Default image
        self.direction = 0
        
        self.size = size
        self.surface = surface
        self.gravity = 0.4
        self.speed = 6
        self.jump_force = 0.4 * size

        self.pos = 0.5 * pygame.Vector2(surface.get_size()) - 0.5 * pygame.Vector2(self.image.get_size())
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, self.gravity)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.standing_on_ground = False
        self.jumped = False

    def update_animation(self):
        if self.counter > self.walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            elif self.direction == -1:
                self.image = self.images_left[self.index]
        # If player stops moving, reset animation to the first frame
        elif self.vel.x == 0:
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            elif self.direction == -1:
                self.image = self.images_left[self.index]

    def draw(self, cam_pos, map: Map, screen: pygame.Surface):
        if self.size != map.map_rect_width:
            self.size = map.map_rect_width
            self.image = pygame.transform.scale(self.image, (40, 80))
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.jump_force = 0.4 * self.size
        screen.blit(self.image, self.rect.move(-cam_pos))

    def move(self, map: Map):
        self.standing_on_ground = False
        self.vel += self.acc

        offsetted_rect = self.rect.copy()

        offsetted_rect.x += int(self.vel.x)
        collision_list = [tile for tile in map.map_rects if tile.colliderect(offsetted_rect)]
        for tile in collision_list:
            if self.vel.x < 0:
                offsetted_rect.left = tile.right
                self.vel.x *= 0
            elif self.vel.x > 0:
                offsetted_rect.right = tile.left
                self.vel.x *= 0

        offsetted_rect.y += int(self.vel.y)
        collision_list = [tile for tile in map.map_rects if tile.colliderect(offsetted_rect)]
        for tile in collision_list:
            if self.vel.y < 0:
                offsetted_rect.top = tile.bottom
                if tile == map.start_game_rect:
                    map.start_game_enabled = True
                if tile == map.end_game_rect:
                    map.end_game_enabled = True
                self.vel.y *= 0
            elif self.vel.y > 0:
                offsetted_rect.bottom = tile.top
                self.vel.y *= 0
                self.standing_on_ground = True

        # Check for collision with exit_group
        exit_collision = pygame.sprite.spritecollideany(self, map.exit_group)
        if exit_collision:
            print("Collided with an exit")
            map.map1_enabled = True

        self.rect = offsetted_rect
        self.pos = pygame.Vector2(self.rect.center)
        self.vel.x *= 0

    def jump(self):
        self.vel.y = -self.jump_force
