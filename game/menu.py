import pygame
from game import WINDOW_WIDTH, WINDOW_HEIGHT, TICK_RATE
from flappy_bird.characters import *
from flappy_bird.objects import Character


class  Menu:

    OPTIONS = [
        pygame.image.load("./assets/menu/button_ai.png"),  # This is the TEST AI button
        pygame.image.load("./assets/menu/button_solo.png"),  # This is the SOLO button
        pygame.image.load(
            "./assets/menu/button_multiplayer.png"
        ),  # This is the AI VS PLAYER button
    ]
    TITLE = "FLAPPY BIRD"
    INTRO = "KAIN INOM GALA PRESENTS..."
    
    selected_mode = 0
    run = True

    def __init__(self, win):
        self.win = win
        # for text
        # This need to change and need to be centralized
        self.font_text = pygame.font.Font("./assets/fonts/retropix.ttf", 20)
        self.font_title = pygame.font.Font("./assets/fonts/retropix.ttf", 50)
        self.background_image = pygame.transform.scale(
            pygame.image.load("./assets/menu/menu.png"), (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.current_character = 0
        self.selected_character = Character.characters_available()[self.current_character](50, 670)
        self.run = True
        self.clock = pygame.time.Clock()

    def draw(self):
        self.win.fill((0, 0, 0))  # Fills the window with black
        self.win.blit(self.background_image, (0, 0))
        # Draws the title and intro ============
        title = self.font_title.render(self.TITLE, 1, "#F7DB6E")
        intro = self.font_text.render(self.INTRO, 0.2, "#F7DB6E")
        # Draws the title
        self.win.blit(intro, (WINDOW_WIDTH / 2 - intro.get_width() / 2, 170))
        self.win.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 220))
        # ======================================
        # Selection related code
        # Draws the options
        for i in range(len(self.OPTIONS)):
            if i == self.selected_mode:
                selected_button = (pygame.transform.scale(self.OPTIONS[i], (180, 45))) # When selected, resize the button larger
            else:
                selected_button = (
                    pygame.transform.scale(self.OPTIONS[i], (160, 40)) # When not selected, resize the button smaller
                )

            self.win.blit(
                selected_button,
                (
                    WINDOW_WIDTH / 2 - selected_button.get_width() / 2, # Center the buttons
                    320 + i * 40 + i * 5
                )
            )

        # Draws the character selection
        
        if self.selected_mode == 3:
            for i, character in enumerate(Character.characters_available()):
                if i == self.current_character:
                    self.selected_character = character(50, 670)
        else:
            self.win.blit(
                self.selected_character.img,
                (50, 670),
            )
        
        self.selected_character.draw(self.win)


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
                        # When the cursor is on the options
                        self.selected_mode = (self.selected_mode + 1) % (len(
                            self.OPTIONS
                        ) + 1)
                    if event.key == pygame.K_UP:
                        # When the cursor is on the options
                        self.selected_mode = (self.selected_mode - 1) % (len(
                            self.OPTIONS
                        ) + 1)
                    if event.key == pygame.K_RETURN  or event.key == pygame.K_SPACE:
                        self.selected_mode_option()
                        break

                    if self.selected_mode == 3:
                        # when the cursor is on the character selection
                        if event.key == pygame.K_LEFT:
                            self.current_character = (self.current_character - 1) % len(
                                Character.characters_available()
                            )
                        if event.key == pygame.K_RIGHT:
                            self.current_character = (self.current_character + 1) % len(
                                Character.characters_available()
                            )


    def selected_mode_option(self):
        """Handles the selected mode"""
        if self.selected_mode == 0:
            print("TEST AI")
            self.run = False
        elif self.selected_mode == 1:
            print("SOLO")
            self.run = False
        elif self.selected_mode == 2:
            print("AI VS PLAYER")
            self.run = False
        elif self.selected_mode == 3:
            # Pass the character choice to the game
            pass
        
        self.selected_character.set_default_pos()

