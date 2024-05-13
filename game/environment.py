from calendar import c
import pygame
from flappy_bird import SPEED_CHANGE_EVERY
from flappy_bird.maps import MapHandler
from flappy_bird.objects import Character
from game import WINDOW_WIDTH, TICK_RATE
import time
class Environment:
    """The environment class for the game"""
    def __init__(self, win, maps:MapHandler, char:Character):
        self.win = win
        self.map = maps
        self.char = char
        self.is_running = True
        self.is_finished = False
        self.is_paused = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("./assets/fonts/retropix.ttf", 20)
        self.score = 0
        self.selected_option = 0
        self.last_screenshot_time = time.time()

    def loop(self):
        """Runs the game loop"""
        print("game loop start")
        while self.is_running:
            #print(self.is_running)
            self.clock.tick(TICK_RATE) # Sets the tick rate of the game, TICK_RATE reference from game/__init__.py
            
            self._controls_loop() # Handles the controls loop for the game

            self._collided() # Handles the collides of the character with the floor and pipes
            
            if not self.is_finished and not self.is_paused: # This will stop the game loop if the game is finished
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
                    # If the character has passed the pipe, add a new pipe and increment the score
                    self.score += 1
                    self.map.pipes.append(self.map.create_pipe())
                    add_pipe = False
                    
                    if self.score % SPEED_CHANGE_EVERY == 0:
                        self.map.set_speed_map(self.map.PIPE_VEL + 1) # Increase the speed of the map every 5 points
                # Remove the pipes that are off the screen
                for r in rem:
                    self.map.pipes.remove(r)

                self.char.move() # Handles the movement of the character
                self.map.floor.move() # Handles the movement of the floor

                self.draw() # Draws the game
            
                
            
        print("game is no longer running")
            

    
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
        """Restarts the game if the game is finished"""
        # Resart the game
        if self.is_finished:
            new_map = self.map.new_map()
            self.map.change_map(new_map)
            self.char.y = 350
            self.map.pipes = [self.map.create_pipe()]
            self.score = 0
            self.run()
    
    def exit_mode(self):
        """Exits mode if game is finished"""
        print("exit mode")
        self.is_running = False
        print(self.is_running)
        # Calls loop to stop the while loop and return to menu
        # removed the self.loop()
            
    
    def run(self):
        """Runs the menu loop"""
        self.is_finished = False
        self.is_running = True
        self.is_paused = False
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
    
    def clear(self):
        self.char.x = 700 # temporary solutions which clear out the board
        self.char.y = 600
        self.char = None
        self.map = None
        
        pygame.display.update()