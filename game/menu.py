import pygame
from game import WINDOW_WIDTH, WINDOW_HEIGHT, TICK_RATE


class Menu:

    OPTIONS = [
        pygame.image.load("./assets/menu/button_ai.png"),  # This is the TEST AI button
        pygame.image.load("./assets/menu/button_solo.png"),  # This is the SOLO button
        pygame.image.load(
            "./assets/menu/button_multiplayer.png"
        ),  # This is the AI VS PLAYER button
    ]
    TITLE = "FLAPPY BIRD"
    INTRO = "KAIN INOM GALA PRESENTS..."
    selected_character = None
    selected_mode = 0
    run = True

    def __init__(self, win):
        self.win = win
        # for text
        self.font_text = pygame.font.Font("./assets/fonts/retropix.ttf", 20)
        self.font_title = pygame.font.Font("./assets/fonts/retropix.ttf", 50)
        self.background_image = pygame.image.load("./assets/menu/menu.png")
        self.background_image = pygame.transform.scale(
            self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        self.run = True
        self.clock = pygame.time.Clock()

    def draw(self):
        self.win.fill((0, 0, 0))  # Fills the window with black
        self.win.blit(self.background_image, (0, 0))
        # Text related
        title = self.font_title.render(self.TITLE, 1, "#F7DB6E")
        intro = self.font_text.render(self.INTRO, 0.2, "#F7DB6E")
        # Draws the title
        self.win.blit(intro, (WINDOW_WIDTH / 2 - intro.get_width() / 2, 170))
        self.win.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 220))
        # Draws the options
        for i in range(len(self.OPTIONS)):
            # text = self.font_text.render("TEXT", 1, (255, 255, 255))

            # self.win.blit(self.button_ai, (WINDOW_WIDTH/2 - self.button_ai.get_width()/2, 320 + 0 - 10))
            # self.win.blit(self.button_solo, (WINDOW_WIDTH/2 - self.button_solo.get_width()/2, 320 + 50 - 10))
            # self.win.blit(self.button_multiplayer, (WINDOW_WIDTH/2 - self.button_multiplayer.get_width()/2, 320 + 100 - 10))
            # self.win.blit(self.font_text.render(
            #         "EXIT", 1, (255, 255, 255)), (WINDOW_WIDTH/2 - text.get_width()/2, 320 + 150 - 10))

            if i == self.selected_mode:
                selected_button = (pygame.transform.scale(self.OPTIONS[i], (200, 45))) # When selected, resize the button larger

            else:
                selected_button = (
                    pygame.transform.scale(self.OPTIONS[i], (175, 40)) # When not selected, resize the button smaller
                )

            self.win.blit(
                selected_button,
                (
                    WINDOW_WIDTH / 2 - selected_button.get_width() / 2, # Center the buttons
                    320 + i * selected_button.get_height()
                )
            )

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
                        self.selected_mode = (self.selected_mode + 1) % len(
                            self.OPTIONS
                        )
                    if event.key == pygame.K_UP:
                        self.selected_mode = (self.selected_mode - 1) % len(
                            self.OPTIONS
                        )
                    if event.key == pygame.K_RETURN:
                        self.selected_mode_option()

    def selected_mode_option(self):
        if self.selected_mode == 0:
            print("TEST AI")
            self.run = False
        elif self.selected_mode == 1:
            print("SOLO")
            self.run = False
        elif self.selected_mode == 2:
            print("AI VS PLAYER")
            self.run = False
        else:
            self.run = False
            pygame.quit()
