import pygame
from .map import Map

class Player:
    def __init__(self, img_path: str, size: float, surface: pygame.Surface) -> None:
        # self.img = pygame.image.load(img_path)
        self.img = pygame.Surface((size, size))
        self.img = pygame.transform.scale(self.img, (self.img.get_width() * size / self.img.get_height(), size))
        self.size = size
        self.img.fill((100, 100, 255))

        self.gravity = 0.4
        self.speed = 6
        self.jump_force = 0.4 * size

        self.pos = 0.5 * pygame.Vector2(surface.get_size()) - 0.5 * pygame.Vector2(self.img.get_size())
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, self.gravity)

        self.surface = surface

        self.rect = self.img.get_rect()
        self.rect.centerx = int(self.pos.x)
        self.rect.centery = int(self.pos.y)

        self.standing_on_ground = False

    def draw(self, cam_pos, map: Map):
        if self.size != map.map_rect_width:
            self.size = map.map_rect_width
            self.img = pygame.transform.scale(self.img, (self.size, self.size))
            self.rect = self.img.get_rect()
            self.rect.centerx = int(self.pos.x)
            self.rect.centery = int(self.pos.y)
            self.jump_force = 0.4 * self.size
        self.surface.blit(self.img, self.rect.move(-cam_pos))

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
                self.vel.y *= 0
                if tile == map.start_game_rect:
                    map.start_game_enabled = True
                if tile == map.end_game_rect:
                    map.end_game_enabled = True
            if self.vel.y > 0:
                offsetted_rect.bottom = tile.top
                self.vel.y *= 0
                self.standing_on_ground = True
                if tile == map.map1_rect:
                    map.map1_enabled = True

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
