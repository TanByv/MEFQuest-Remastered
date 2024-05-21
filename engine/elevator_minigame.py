import textwrap
import pygame
import sys

class ElevatorMiniGame:
    def __init__(self):
        # Pygame başlatma
        pygame.init()

        # Ekran ayarları
        self.width, self.height = 1200, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Repairing the Elevator')

        # Renkler
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 128)

        # Font ayarları
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 50)

        # Sorular ve cevaplar
        self.questions = [
            ("The organizational changes in processor design have primarily been focused on increasing instruction-level parallelism.", True),
            ("GPUs are capable of running operating systems.", False),
            ("With superscalar organization increased performance can be achieved by increasing the number of parallel pipelines.", True),
            ("The caches hold recently accessed data.", True)
        ]

        # Resmi yükle
        image_path = '/Users/enes/Downloads/game/img/guy1.png'
        self.image = pygame.image.load(image_path)
        self.image_rect = self.image.get_rect()
        self.image_rect.bottomleft = (90, self.height)

    def start_screen(self):
        while True:
            self.screen.fill(self.BLACK)

            # Başlangıç ekranı metni
            start_text = self.large_font.render("Now you should give the correct answers to the following questions.", True,
                                                self.WHITE)
            self.screen.blit(start_text, (self.width // 2 - start_text.get_width() // 2, self.height // 2 - 50))

            # Start butonu
            start_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 50, 200, 50)
            pygame.draw.rect(self.screen, self.BLUE, start_button)

            # Start butonu metni
            start_text_button = self.font.render("Start", True, self.WHITE)
            self.screen.blit(start_text_button, (start_button.x + 60, start_button.y + 10))

            # Start butonu ikonu
            pygame.draw.polygon(self.screen, self.WHITE, [(start_button.x + 20, start_button.y + 15),
                                                           (start_button.x + 20, start_button.y + 35),
                                                           (start_button.x + 35, start_button.y + 25)])
            self.screen.blit(self.image, self.image_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if start_button.collidepoint(mouse_pos):
                        return  # Başlangıç ekranından çık ve oyunu başlat

    def game_loop(self):
        score = 0
        for question, correct_answer in self.questions:
            # Soruyu ekrana yazdır
            self.screen.fill(self.BLACK)
            lines = textwrap.wrap(question, width=70)  # Metni 60 karakter genişliğinde kır

            # Metin yüksekliği hesapla
            total_height = sum(self.font.size(line)[1] + 5 for line in lines)

            # Metni dikey olarak ortalamak için başlangıç yüksekliğini hesapla
            y_offset = (self.height - total_height) // 4 + 60

            for line in lines:
                question_surface = self.font.render(line, True, self.WHITE)
                # Metni yatay olarak ortala
                x_offset = (self.width - question_surface.get_width()) // 2
                self.screen.blit(question_surface, (x_offset, y_offset))
                y_offset += question_surface.get_height() + 5  # Satır aralığını ayarla

            # True ve False butonları
            true_button = pygame.Rect(400, 350, 100, 50)
            false_button = pygame.Rect(700, 350, 100, 50)

            # Butonları çiz
            pygame.draw.rect(self.screen, self.GREEN, true_button)
            pygame.draw.rect(self.screen, self.RED, false_button)

            # Butonlara metin ekle
            true_text = self.font.render('True', True, self.WHITE)
            false_text = self.font.render('False', True, self.WHITE)
            self.screen.blit(true_text, (true_button.x + 20, true_button.y + 10))
            self.screen.blit(false_text, (false_button.x + 10, false_button.y + 10))

            # Resmi ekrana çiz
            self.screen.blit(self.image, self.image_rect)

            pygame.display.flip()

            # Kullanıcı girdisini bekleyin
            answered = False
            while not answered:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if true_button.collidepoint(mouse_pos):
                            answered = True
                            if correct_answer == True:
                                score += 1
                        elif false_button.collidepoint(mouse_pos):
                            answered = True
                            if correct_answer == False:
                                score += 1

        # Skoru göster
        self.screen.fill(self.BLACK)
        score_text = self.font.render(f'Your score is: {score}/{len(self.questions)}', True, self.WHITE)
        # Skor metnini ortala
        score_x = (self.width - score_text.get_width()) // 2
        self.screen.blit(score_text, (score_x, 100))
        if score == 4:
            congrats_text = self.font.render(f'Congratulations you fixed the elevator', True, self.WHITE)
        else:
            congrats_text = self.font.render(f'--No--', True, self.WHITE)

        # Tebrik metnini ortala
        congrats_x = (self.width - congrats_text.get_width()) // 2
        self.screen.blit(congrats_text, (congrats_x, 200))
        self.screen.blit(self.image, self.image_rect)  # Skor ekranında da resmi göster
        pygame.display.flip()
        pygame.time.wait(1000)

        # Skoru return et
        return score

def run_game():
    game = ElevatorMiniGame()
    game.start_screen()
    score = game.game_loop()
    if score == 4:
        return True
    else:
        return False
