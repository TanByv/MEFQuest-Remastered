import csv
import os
import time
import pygame
import random

# Constants
WIDTH, HEIGHT = 1600, 900
WHITE, BLACK, GRAY, RED = (255, 255, 255), (0, 0, 0), (100, 100, 100), (255, 0, 0)
KEYS_N = ["Q", "W", "E", "A", "S", "D"]


class MiniGame:
    def __init__(self, player_sprite, csv_name):
        # Constants
        self.WIDTH, self.HEIGHT = 900, 700
        self.WHITE, self.BLACK, self.GRAY, self.RED = (255, 255, 255), (0, 0, 0), (100, 100, 100), (255, 0, 0)
        self.KEYS_N = ["Q", "W", "E", "A", "S", "D"]

        self.player_sprite = player_sprite
        self.csv_filename = f"assets/dialog/{csv_name}.csv"
        self.csv_filename2 = f"assets/dialog/{csv_name}2.csv"

        self.next_message_triggered = False

        self.buttons = []
        self.player1 = None
        self.player2 = None
        self.box1 = None
        self.box2 = None
        self.box_guide = None
        self.box_counter = None
        self.box_messages = None
        self.current_index = 0
        self.check = False

        self.init_game()

    def read_messages_from_csv(self, csv_filename):
        messages = []
        with open(csv_filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Satır boş değilse
                    message = ' '.join(row)  # CSV'deki sütunları birleştirerek bir metin oluştur
                    messages.append(message)
        return messages

    def init_game(self):
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mini Game")
        random.shuffle(KEYS_N)  # shuffle yaparak arrayi karıştırır
        self.buttons = [Button(150 + i * 100, 500, self.KEYS_N[i]) for i in range(len(self.KEYS_N))]
        self.player1 = Player(650, 170, 150, 200, self.player_sprite)
        self.player2 = Player(100, 70, 75, 100, "guy1")
        self.box1 = MessageBox(200, 50, 600, 150, "", font_size=20)
        self.box2 = MessageBox(60, 230, 600, 150, "", font_size=20)
        self.box_guide = MessageBox(150, 600, 600, 50, "Press n to continue!")
        self.box_counter = MessageBox(335, 400, 200, 50, "5", font_size=40)
        self.box_messages = self.read_messages_from_csv(self.csv_filename)
        self.box_timer = MessageBox(-10, 580, 200, 50, "", font_size=25)
        global next_message_triggered, box_messages, timer, global_time
        next_message_triggered = False
        self.current_index = 0
        self.boxInd = [0]
        self.global_time = 0
        self.timer = 0

        def drawAllButtons():
            self.box_counter.set_text("Fight!")
            self.box_counter.drawChatB(screen)
            n=0
            for button in self.buttons:
                button.text = KEYS_N[n]  # Yeni metni ayarla
                button.drawButton(screen)
                n += 1

        def resetAllButtons():
            random.shuffle(KEYS_N)  # shuffle yaparak arrayi karıştırır
            for button in self.buttons:
                button.release()

        def next_message():
            global next_message_triggered
            if self.box_messages:
                if self.boxInd[0] == 0:
                    self.box1.set_text(self.box_messages.pop(0))  # İlk mesajı alıp kutuya yaz
                    self.boxInd[0] = 1
                elif self.boxInd[0] == 1:
                    self.box2.set_text(self.box_messages.pop(0))  # İlk mesajı alıp kutuya yaz
                    self.boxInd[0] = 0
            else:
                self.next_message_triggered = True
                if self.player1.number == 100:
                    self.box_guide.set_text("Press Space for fight")
                    self.box_guide.drawChatB(screen)
                elif self.player1.number == 0:
                    self.check = True

        def true_set():
            resetAllButtons()
            drawAllButtons()

        def drawAllCharacters():
            screen.fill(BLACK)  # Ekranı siyahla doldurarak eski değerleri temizle
            self.player1.drawChar(screen)
            self.player2.drawChar(screen)
            pygame.display.flip()

        def random_number():
            return random.randint(10, 25)

        def start_fight():
            i = 3
            while i > 0:
                self.box_counter.set_text(str(i))
                drawBlackSquare(screen, 400, 400, 60, 60)
                self.box_counter.drawChatB(screen)
                pygame.display.flip()
                time.sleep(1)
                i -= 1
            drawBlackSquare(screen, 400, 400, 60, 60)
            self.box_counter.set_text("Fight!")
            self.box_guide.set_text("Print the numbers in the correct order")
            self.box_counter.drawChatB(screen)

        def check_players_health():
            if self.player1.number <= 0:
                drawBlackSquare(screen, 400, 400, 60, 60)
                self.box_counter.set_text("You Win!")
                self.box_counter.drawChatB(screen)
                check_csv2()
            elif self.player2.number <= 0:
                self.check = True

        def set_global_time():
            global global_time, timer
            self.global_time = time.time()
            self.timer = 1

        def get_elapsed_time():
            global global_time
            current_time = time.time()
            elapsed_time = current_time - self.global_time
            return 30 - elapsed_time

        def check_csv2():
            global next_message_triggered, box_messages
            if os.path.exists(self.csv_filename2):
                self.next_message_triggered = False
                self.box_guide.set_text("Press n to continue!")
                self.box_messages = self.read_messages_from_csv(self.csv_filename2)
            else:
                self.check = True

        def drawBlackSquare(screen, x, y, width, height):
            pygame.draw.rect(screen, BLACK, (x, y, width, height))  # Kareyi siyahla doldur

        drawAllCharacters()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.KEYDOWN:
                    if self.next_message_triggered:
                        if event.key == pygame.K_SPACE:
                            start_fight()
                            drawAllButtons()
                            set_global_time()

                        elif pygame.key.name(event.key).upper() in KEYS_N:

                            if pygame.key.name(event.key).upper() == KEYS_N[self.current_index]:
                                self.buttons[self.current_index].press()
                                drawAllButtons()
                                self.current_index += 1

                                if self.current_index == 6:
                                    self.player1.number -= 40 #random_number()
                                    if self.player1.number < 0:
                                        self.player1.number = 0
                                    drawAllCharacters()  # Karakterleri yeniden çiz
                                    true_set()
                                    self.current_index = 0
                                    check_players_health()

                            elif pygame.key.name(event.key).upper() != KEYS_N[self.current_index]:
                                self.player2.number -= (random_number() // 10) * 3
                                if self.player2.number < 0:
                                    self.player2.number = 0
                                    check_players_health()

                                drawAllCharacters()  # Karakterleri yeniden çiz
                                resetAllButtons()
                                drawAllButtons()
                                self.current_index = 0

                    elif event.key == pygame.K_n:
                        next_message()


            self.box1.drawChatW(screen)
            self.box2.drawChatW(screen)
            self.box_guide.drawChatB(screen)
            pygame.display.flip()
            self.box_timer.drawChatB(screen)

            if self.next_message_triggered and self.timer == 1:
                drawBlackSquare(screen, 5, 600, 200, 50)
                self.box_timer.set_text(str(int(get_elapsed_time())))
                self.box_timer.drawChatB(screen)

                if get_elapsed_time() < 0 or self.check:
                    return

class MessageBox:
    def __init__(self, x, y, width, height, text='', font_size=24, bg_color=BLACK, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = pygame.font.SysFont('comicsans', font_size)
        self.set_text(text)

    def set_text(self, text):
        self.text = text
        self.rendered_text, self.text_rects = self.render_multiline_text(text)

    def render_multiline_text(self, text):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= self.rect.width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        line_height = self.font.get_linesize()
        total_height = len(lines) * line_height
        rendered_surface = pygame.Surface((self.rect.width, total_height), pygame.SRCALPHA)
        rendered_surface.fill(self.bg_color)

        text_rects = []
        for i, line in enumerate(lines):
            rendered_line = self.font.render(line, True, self.text_color)
            line_width = self.font.size(line)[0]
            line_rect = rendered_line.get_rect(center=(self.rect.width // 2, i * line_height + line_height // 2))
            rendered_surface.blit(rendered_line, (self.rect.width // 2 - line_width // 2, i * line_height))
            text_rects.append(line_rect)

        return rendered_surface, text_rects

    def drawChatW(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        centered_y = (self.rect.height - self.rendered_text.get_height()) // 2
        screen.blit(self.rendered_text, (self.rect.x, self.rect.y + centered_y))

    def drawChatB(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        centered_y = (self.rect.height - self.rendered_text.get_height()) // 2
        screen.blit(self.rendered_text, (self.rect.x, self.rect.y + centered_y))


class Player():
    def __init__(self, x, y, height, width, sprites):
        self.img = pygame.image.load(f'assets/sprites/{sprites}.png')
        self.image = pygame.transform.scale(self.img, (height, width))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.number = 100  # sonradan parametre olarak ekleyebilirsin

    def drawChar(self, screen):
        screen.blit(self.image, self.rect)
        font = pygame.font.SysFont('comicsans', 24)
        text_surface = font.render(str(self.number), True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 25, self.rect.y + self.rect.height + 5))

class Button:
    def __init__(self, x, y, text=''):
        self.rect = pygame.Rect(x, y, 80, 80)
        self.color = WHITE
        self.text = text

    def drawButton(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.text:
            font = pygame.font.SysFont('comicsans', 40)
            text_surface = font.render(self.text, True, BLACK)
            screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def press(self):
        self.color = GRAY

    def release(self):
        self.color = WHITE
