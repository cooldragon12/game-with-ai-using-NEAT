from flappy_bird.objects import Pipe
from .environment import Environment
import pygame
from game import WINDOW_WIDTH, WINDOW_HEIGHT
class TestAI(Environment):
    def controls(self, event):
        # Change this depending on the mode
        pass

    def collide_handler(self):
        self.is_finished = True 
        self.restart()

class Solo(Environment):
    def collide_handler(self):
        self.is_finished = True
        self.game_over_prompt()
        
    def controls(self, event):
        """Handles the controls for the game"""
        if event.type == pygame.KEYDOWN:
            if self.is_finished:
                # user selects which option to choose after game over
                if event.key == pygame.K_LEFT:
                    # user selects restart
                    self.selected_option = 0
                    # redraw grame over prompt
                    self.game_over_prompt()
                if event.key == pygame.K_RIGHT:
                    # user selects exit
                    self.selected_option = 1
                    # redraw grame over prompt
                    self.game_over_prompt()
                # user confirms decision
                if event.key == pygame.K_RETURN:
                    # restart                 
                    if self.selected_option == 0:
                        return self.restart()
                    # exit to menu
                    else:
                        return self.exit_mode()


            if not self.is_finished:     
                if event.key == pygame.K_SPACE:
                    return self.char.jump()
                
    def game_over_prompt(self):
        """This will prompt the game over message"""
        # draw game over title
        gameover_font = pygame.font.Font("./assets/fonts/Minercraftory.ttf", 45)
        gameover_text = gameover_font.render("GAME OVER", True, (255, 255, 255))
        gameover_text_rect = gameover_text.get_rect(center=(WINDOW_WIDTH/2, 150))
        self.win.blit(gameover_text, gameover_text_rect)
        # draw score
        score_font = pygame.font.Font("./assets/fonts/Minercraftory.ttf", 25)
        score_text = score_font.render("Score " + str(self.score), 1, (255,255,255)) 
        score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, 220))
        self.win.blit(score_text, score_text_rect)
        # draws rectangle
        # rectangle border
        pygame.draw.rect(self.win, (214,168,74), (45, 245, 410, 210), border_radius=10)
        # rectangle bezel
        pygame.draw.rect(self.win, (255,234,163), (50, 250, 400, 200), border_radius=10)
        # rectangle bezel inside border
        pygame.draw.rect(self.win, (214,168,74), (61, 261, 378, 178), border_radius=10)
        # rectangle inside
        pygame.draw.rect(self.win, (255,234,163), (65, 265, 370, 170), border_radius=10)
        # draw play button
        play = pygame.image.load('./assets/general/play.svg')
        # scale button if it's selected
        if(self.selected_option == 0):
            play = pygame.transform.scale(
                play, (60,65)
            )
            self.win.blit(play, (125, 312))
        else:
            play = pygame.transform.scale(
                play, (50,55)
            )
            self.win.blit(play, (130, 317))
        # draw menu button
        menu = pygame.image.load('./assets/general/menu.svg')
        # scale button if it's selected
        if(self.selected_option == 1):
            menu = pygame.transform.scale(
                menu, (60,65)
            )
            self.win.blit(menu, (295, 312))
        else:
            menu = pygame.transform.scale(
                menu, (50,55)
            )
            self.win.blit(menu, (300, 317))
        pygame.display.update()


    
class AIvsPlayer(Environment):
    pass