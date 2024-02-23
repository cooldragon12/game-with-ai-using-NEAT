import pygame
from game import WINDOW_WIDTH, WINDOW_HEIGHT, TICK_RATE


class Menu:

    OPTIONS = ["TEST AI", "SOLO", "AI VS PLAYER", "Exit"]
    TITLE = "FLAPPY BIRD"
    INTRO = "KAIN INOM GALA PRESENTS..."
    SELECTED = 0
    run = True

    def __init__(self, win):
        self.win = win
        # for text
        self.font_text = pygame.font.Font("./assets/fonts/retropix.ttf", 20)
        self.font_title = pygame.font.Font("./assets/fonts/retropix.ttf", 50)
        self.background_image = pygame.image.load("./assets/menu/menu.png")
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.run = True
        self.clock = pygame.time.Clock()

    def draw(self):
        self.win.fill((0, 0, 0))  # Fills the window with black
        self.win.blit(self.background_image, (0,0))
        # Text related
        title = self.font_title.render(
            self.TITLE, 1, "#F7DB6E")
        intro = self.font_text.render(self.INTRO, 0.2, "#F7DB6E")
        # Draws the title
        self.win.blit(intro, (WINDOW_WIDTH/2 - intro.get_width()/2, 170))
        self.win.blit(title, (WINDOW_WIDTH/2 - title.get_width()/2, 220))
        # Draws the options
        for i in range(len(self.OPTIONS)):
            if i == self.SELECTED:
                text = self.font_text.render(self.OPTIONS[i], 1, (255, 0, 0))
            else:
                text = self.font_text.render(
                    self.OPTIONS[i], 1, (255, 255, 255))
            self.win.blit(
                text, (WINDOW_WIDTH/2 - text.get_width()/2, 320 + i*50))
        pygame.display.update()

    def run_menu(self):
        """Runs the menu loop"""
        while self.run:
            self.clock.tick(TICK_RATE)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.SELECTED = (self.SELECTED + 1) % len(self.OPTIONS)
                    if event.key == pygame.K_UP:
                        self.SELECTED = (self.SELECTED - 1) % len(self.OPTIONS)
                    if event.key == pygame.K_RETURN:
                        self.selected_option()

    def selected_option(self):
        if self.SELECTED == 0:
            print("TEST AI")
            self.run = False
        elif self.SELECTED == 1:
            print("SOLO")
            self.run = False
        elif self.SELECTED == 2:
            print("AI VS PLAYER")
            self.run = False
        else:
            self.run = False
            pygame.quit()
