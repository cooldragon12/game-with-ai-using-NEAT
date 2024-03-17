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
    # Initiate the menu
    menu = Menu(win)
    # This line of code from line 19 to 30 will insert into the menu class, for the map choice
    # Intiate the intance of the Character
    # char = Bird(230, 350)
    # Initiate the base
    # Initiate the Map
    maps = MapHandler()   
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
        # The pause of the game is not yet working or the game loop 
        mode = Environment.modes()[menu.selected_mode](win, maps, menu.selected_character)
        mode.run()
        
        if mode.is_finished == True and mode.is_running == False:
            mode.clear()
            del mode
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

