from calendar import c
import pygame

from flappy_bird.maps import MapHandler
from flappy_bird.objects import Character
from game import WINDOW_WIDTH
class Environment:
    def __init__(self, win, maps:MapHandler, char:Character):
        self.win = win
        self.map = maps
        self.char = char
        self.is_running = True
        self.is_finished = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("./assets/fonts/retropix.ttf", 20)
        self.score = 0

    def loop(self):
        """Runs the game loop"""
        while self.is_running:
            self.clock.tick(30)
            
            self._controls_loop()

            self._collided() # Handles the collides of the character with the floor and pipes
            
            if not self.is_finished: # This will stop the game loop if the game is finished
                rem = []
                add_pipe = False 
                for pipe in self.map.pipes:
                    # If the pipe is off the screen, remove it
                    if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                        rem.append(pipe) 
                    # If the pipe is not passed and the character has passed it, add a new pipe
                    if not pipe.passed and pipe.x < self.char.x:
                        pipe.passed = True
                        add_pipe = True
                    
                    pipe.move()
                    
                if add_pipe:
                    self.score += 1
                    self.map.pipes.append(self.map.create_pipe())
                    add_pipe = False
                
                for r in rem:
                    self.map.pipes.remove(r)

                self.char.move() # Handles the movement of the character
                self.map.floor.move() # Handles the movement of the floor

                self.draw()
            

    
    def collide_handler(self):
        """Handles the collision of the character with the floor and pipes
        
        Change this depending on the game
        """
        pass
    
    def _collided(self):
        """This handles the collision of the character with the floor and pipes"""
        if self.map.floor.collide(self.char): # If the character collide with the floor
            return self.collide_handler()
        for pipe in self.map.pipes: # If the character collide with the pipes
            if pipe.collide(self.char):
                return self.collide_handler()

    def controls(self, event):
        """Handles the controls for the game"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.char.jump()

    def _controls_loop(self):
        """Handles the controls loop for the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                pygame.quit()
                quit()
            self.controls(event)

    def restart(self):
        # Resart the game
        if self.is_finished:
            new_map = self.map.new_map()
            self.map.change_map(new_map)
            self.char.y = 350
            self.map.pipes = [self.map.create_pipe()]
            self.score = 0
            self.run()
            
    
    def run(self):
        """Runs the menu loop"""
        self.is_finished = False
        self.is_running = True
        self.loop()
            
    def draw(self):
        self.win.blit(self.map.bg, (0, 0))

        for pipe in self.map.pipes:
            pipe.draw(self.win)
        
        text = self.font.render("Score: " + str(self.score), 1, (255,255,255)) 
        self.win.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))

        self.map.floor.draw(self.win)
        self.char.draw(self.win)
        pygame.display.set_caption("Flappy Bird")
        pygame.display.update()
    
    @classmethod
    def modes(cls):
        return cls.__subclasses__()