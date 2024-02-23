import pygame

from flappy_bird.maps import Map
from flappy_bird.objects import Character, Pipe
from game import WINDOW_WIDTH
class Environment:
    def __init__(self, win, maps:Map, char:Character):
        self.win = win
        self.map = maps
        self.char = char
        self.run = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("./assets/fonts/retropix.ttf", 20)
        self.score = 0

    def loop(self):
        """Runs the game loop"""
        while self.run:
            self.clock.tick(30)

            self._controls_loop()

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
                self.map.pipes.append(Pipe(700))
                add_pipe = False
            
            for r in rem:
                self.map.pipes.remove(r)

            self._collided() # Handles the collides of the character with the floor and pipes
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
        if self.map.floor.collide(self.char):
            self.collide_handler()
        for pipe in self.map.pipes:
            if pipe.collide(self.char):
                self.collide_handler()

    def controls(self, event):
        """Handles the controls for the game"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.char.jump()

    def _controls_loop(self):
        """Handles the controls loop for the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                quit()
            self.event = event
            self.controls(event)
    
    
            
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
