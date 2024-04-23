import pygame


pygame.font.init()
from game import *
from game.menu import Menu
from flappy_bird.characters import *
from game.modes import *
from game.environment import Environment
from flappy_bird.maps import MapHandler


def main():
    # Initiate the window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
    menu = Menu(win)
    
    # The game loop
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

        maps = MapHandler()   
        mode = Environment.modes()[menu.selected_mode](win, maps, menu.selected_character)
        mode.run()
        # clear() resets the character object instantiated in the mode
        mode.clear()
        # deletes both mode and map so a new map can be selected when going to back game mode
        del mode, maps
        menu.run = True
        continue

        # if menu.selected_mode == 3:
        #     # Exit
        #     run = False
        #     break

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()

