# Maps that will be used in the game is put in this file
# Use the Map Class to inherit in different maps
# The Map class will handle the movement of the pipes, the ground and background images, also the game play

import pygame
from .objects import Pipe, Character, Floor, BG_IMG, STATS_FONT
from  game import WINDOW_WIDTH

class Map:
    """Map Class handles the movement of the pipes, the ground and background images, also the game play
    
    Base class for the maps in the game    
    
        """
    def __init__(self, win, char:Character, pipes, Floor:Floor, bg, score):
        self.char = char
        self.pipes = pipes
        self.Floor = Floor
        self.win = win
        self.bg = bg
        self.score = score
        self.run = True
        self.clock = pygame.time.Clock()
    
    def control(self):
        """Runs the game loop"""
        while self.run:
            self.clock.tick(30)
            # Handles events happening 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.char.jump()
            rem = []
            add_pipe = False 
            for pipe in self.pipes:
                if pipe.collide(self.char): # If the bird collides with the pipe
                    pass
                
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe) 
                
                if not pipe.passed and pipe.x < self.char.x:
                    pipe.passed = True
                    add_pipe = True
                
                pipe.move()
                
            if add_pipe:
                self.score += 1
                self.pipes.append(Pipe(700))
                add_pipe = False
            
            for r in rem:
                self.pipes.remove(r)

            if self.Floor.collide(self.char):
                # pygame.quit()
                pass
            self.char.move() # Handles the movement of the character
            self.Floor.move() # Handles the movement of the floor

            self.draw()

    
    def draw(self):
        self.win.blit(BG_IMG, (0, 0))

        for pipe in self.pipes:
            pipe.draw(self.win)
        
        text = STATS_FONT.render("Score: " + str(self.score), 1, (255,255,255)) 
        self.win.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))

        self.Floor.draw(self.win)
        self.char.draw(self.win)
        pygame.display.set_caption("Flappy Tite")
        pygame.display.update()
