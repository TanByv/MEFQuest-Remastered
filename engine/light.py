import pygame
import pygame.gfxdraw

def our_angle_to(vec1, vec2):
    angle = vec1.angle_to(vec2)
    return min(angle, 360 - angle)

class LightSource:
    def __init__(self, surface, pos, color, strength):
        self.pos = pos
        self.color = color
        self.strength = strength
        self.surface = surface

        self.light = pygame.image.load("assets/sprites/light.jpg")

        self.light = pygame.transform.scale(
            self.light,
            [self.strength * min(self.surface.get_size()) / min(self.light.get_size())] * 2
        )

        self.texture = pygame.Surface(self.surface.get_size())
        self.texture.fill((255, 0, 0))
        self.shadow_surface = pygame.Surface(self.surface.get_size())

    def show(self, rects, cam_pos):
        self.shadow_surface.fill(self.color)
        self.texture.fill((0, 0, 0))
        for rect in rects:
            points = [
                    pygame.Vector2(rect.topleft),
                    pygame.Vector2(rect.bottomleft),
                    pygame.Vector2(rect.topright),
                    pygame.Vector2(rect.bottomright),
                    ]
            highest_pair = (points[0], points[1])
            highest_angle = our_angle_to(points[0] - self.pos, points[1] - self.pos)

            for i in range(len(points)):
                for j in range(len(points)):
                    angle = our_angle_to(points[i] - self.pos, points[j] - self.pos)
                    if angle >= highest_angle:
                        highest_angle = angle
                        highest_pair = (points[i], points[j])
            req_points = [
                    highest_pair[0],
                    highest_pair[0] + self.strength * (highest_pair[0] - self.pos).normalize(),
                    highest_pair[1] + self.strength * (highest_pair[1] - self.pos).normalize(),
                    highest_pair[1],
                    ]
            for p in req_points:
                p -= cam_pos
            pygame.draw.polygon(self.shadow_surface, (0, 0, 0), req_points)

        self.texture.blit(
                (self.light),
                self.pos - 0.5 * pygame.Vector2(self.light.get_size()) - cam_pos
                )
        self.shadow_surface.blit(self.texture, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.surface.blit(self.shadow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)




