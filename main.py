import pygame

pygame.font.init()
from flappy_bird.maps import MapHandler
from flappy_bird.characters import Bird
from game import *
from game.menu import Menu
from game.modes import TestAI, Solo, AIvsPlayer



def main():
    # Initiate the window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))    
    # Initiate the menu
    menu = Menu(win)
    # This line of code from line 19 to 30 will insert into the menu class, for the map choice

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
        if menu.selected_mode == 0:
            # Test AI 
            char = Bird(230, 350)
            maps = MapHandler()  
            test = TestAI(win, maps, char)
            test.run()
            # Deletes all instances related to mode for a full restart
            del test, char, maps
            # Proceed to loop menu again
            menu.run = True
        elif menu.selected_mode == 1:
            # Solo
            char = Bird(230, 350)
            maps = MapHandler()  
            solo = Solo(win, maps, char)
            solo.run()
            # Deletes all instances related to mode for a full restart
            del solo, char, maps
            # Proceed to loop menu again
            menu.run = True
        elif menu.selected_mode == 2:
            # AI vs Player
            char = Bird(230, 350)
            maps = MapHandler()  
            ai_vs_player = AIvsPlayer(win, maps, char)
            ai_vs_player.run()
            # Deletes all instances related to mode for a full restart
            del ai_vs_player, char, maps
            # Proceed to loop menu again
            menu.run = True

        elif menu.selected_mode == 3:
            # Exit
            run = False
            break

    pygame.quit()
    quit()

    



if __name__ == "__main__":
    main()

