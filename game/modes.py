from .environment import Environment
import pygame

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
                if event.key == pygame.K_SPACE:
                    return self.restart()
            if not self.is_finished:     
                if event.key == pygame.K_SPACE:
                    return self.char.jump()
                
    def game_over_prompt(self):
        """This will prompt the game over message"""
        # create a box that containe the game over message
        pygame.draw.rect(self.win, (0, 0, 0), (100, 200, 300, 200))
        # create the game over message
        game_over = self.font.render("Game Over", True, (255, 255, 255))
        # create the restart message
        restart = self.font.render("Press Space to Restart", True, (255, 255, 255))
        # draw the game over message
        self.win.blit(game_over, (150, 250))
        # draw the restart message
        self.win.blit(restart, (150, 300))
        # update the display
        pygame.display.update()

    
class AIvsPlayer(Environment):
    pass