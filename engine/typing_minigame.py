from time import sleep
import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (100, 100, 100)
KEYS = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_a, pygame.K_s, pygame.K_d]
KEY_NAMES = {pygame.K_q: 'Q', pygame.K_w: 'W', pygame.K_e: 'E', pygame.K_a: 'A', pygame.K_s: 'S', pygame.K_d: 'D'}

# Button class
class Button:
    def __init__(self, x, y, text=''):
        self.rect = pygame.Rect(x, y, 80, 80)
        self.color = WHITE
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.text:
            font = pygame.font.SysFont('comicsans', 40)
            text_surface = font.render(self.text, True, BLACK)
            screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def is_pressed(self, pos):
        return self.rect.collidepoint(pos)

# Functions
def generate_combinations(num_combinations):
    return [random.sample(range(len(KEYS)), 6) for _ in range(num_combinations)]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Game")
    clock = pygame.time.Clock()
    buttons = [Button(80 + i * 100, 250) for i in range(len(KEYS))]
    num_correct_combinations = 0
    correct_button_count = 0
    start_time = pygame.time.get_ticks()
    elapsed_time = 0
    time_limit = 15000  # 15 seconds

    def update_buttons_text(combination):
        for button, key_index in zip(buttons, combination):
            button.text = KEY_NAMES[KEYS[key_index]]

    combinations = generate_combinations(3)
    current_combination = combinations.pop(0)
    update_buttons_text(current_combination)

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == KEYS[current_combination[0]]:
                    current_combination.pop(0)
                    correct_button_count += 1
                else:
                    print("Wrong key pressed!")
                    current_combination = combinations.pop(0) if combinations else generate_combinations(1)[0]
                    update_buttons_text(current_combination)
                    correct_button_count = 0

        if correct_button_count == len(KEYS):
            print("Point Get!")
            num_correct_combinations += 1
            current_combination = combinations.pop(0) if combinations else generate_combinations(1)[0]
            update_buttons_text(current_combination)
            correct_button_count = 0

        for i, button in enumerate(buttons):
            button.color = GRAY if i < correct_button_count else WHITE
            button.draw(screen)

        pygame.display.flip()

        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time >= time_limit:
            print("Time's up!")
            score = num_correct_combinations * 10
            print("Your score:", score)
            return

        clock.tick(15)

if __name__ == "__main__":
    result = main()
    print(f"Minigame sonucu: {result}")
