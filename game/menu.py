import pygame
from game import WINDOW_WIDTH, WINDOW_HEIGHT

class Menu:

    OPTIONS = ["TEST AI", "SOLO", "AI VS PLAYER", "Exit"]
    TITLE = "FLAPPY TITE"
    SUBTITLE = "Choose a category:"
    INTRO = "Kain inom Gala Presents"
    SELECTED = 0
    run = True
    def __init__(self, win):
        self.win = win
        self.font = pygame.font.SysFont("comicsans", 50)
        self.run = True
        self.clock = pygame.time.Clock()
    
    def draw(self):
        self.win.fill((0,0,0)) # Fills the window with black
        # Text related
        title = self.font.render(self.TITLE, 1, (255,255,255))
        subtitle = self.font.render(self.SUBTITLE, 0.3, (255,255,255))
        intro = self.font.render(self.INTRO, 0.2, (255,255,255))
        # Draws the title
        self.win.blit(title, (WINDOW_WIDTH/2 - title.get_width()/2, 80))
        self.win.blit(subtitle, (WINDOW_WIDTH/2 - subtitle.get_width()/2, 150))
        self.win.blit(intro, (WINDOW_WIDTH/2 - intro.get_width()/2, 200))
        # Draws the options
        for i in range(len(self.OPTIONS)):
            if i == self.SELECTED:
                text = self.font.render(self.OPTIONS[i], 1, (255,0,0))
            else:
                text = self.font.render(self.OPTIONS[i], 1, (255,255,255))
            self.win.blit(text, (WINDOW_WIDTH/2 - text.get_width()/2, 250 + i*50))
        pygame.display.update()
    def run_menu(self):
        """Runs the menu loop"""
        while self.run:
            self.clock.tick(30)
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