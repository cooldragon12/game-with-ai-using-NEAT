from cgi import test
import pygame

pygame.font.init()
from flappy_bird.objects import Pipe, Character, Floor, Background,BG_IMG
from flappy_bird.maps import Map
from game import *
from game.menu import Menu
from game.modes import TestAI, Solo, AIvsPlayer



def main():
    # Initiate the window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # Initiate the menu
    menu = Menu(win)

    # This line of code from line 19 to 30 will insert into the menu class, for the map choice
    # Intiate the intance of the Character
    char = Character(230, 350)
    # Initiate the base
    floor = Floor(730, velocity=6)
    # Initiate the Pipes
    pipes = [Pipe(600)]
    # Initiate the Background
    score = 0
    # Initiate the Map
    maps = Map(pipes, floor, BG_IMG )
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
        
        if menu.SELECTED == 0:
            # Test AI
            test = TestAI(win, maps, char)
            test.loop()
        elif menu.SELECTED == 1:
            # Solo
            solo = Solo(win, maps, char)
            solo.loop()
        elif menu.SELECTED == 2:
            # AI vs Player
            ai_vs_player = AIvsPlayer(win, maps, char)
            ai_vs_player.loop()

        elif menu.SELECTED == 3:
            # Exit
            run = False
            break

        
        

        
        
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()

