import pygame
pygame.font.init()
from flappy_bird.objects import BG_IMG,Pipe, Character, Floor,Background
from flappy_bird.maps import Map
from game import WINDOW_WIDTH, WINDOW_HEIGHT
from game.menu import Menu


def main():
    # Initiate the window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # Initiate the menu
    menu = Menu(win)

    # This line of code from line 19 to 30 will insert into the menu class, for the map choice
    # Intiate the intance of the Character
    char = Character(230, 350)
    # Initiate the base
    base = Floor(730, velocity=6)
    # Initiate the Pipes
    pipes = [Pipe(600)]
    # Initiate the Background
    score = 0
    # Initiate the Map
    maps = Map(win, char, pipes, base, Background, score)

    run = True # Run the game
    # Notice: This run variable is used to control the game loop
    # the main loop
    while run:
        # clock.tick(30)
        # If the menu is running
        if menu.run:
            menu.draw()
            menu.run_menu()
            continue

        # Runs the game loop
        maps.control()
        
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()

