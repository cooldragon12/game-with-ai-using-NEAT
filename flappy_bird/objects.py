import numpy as np
import pygame
import os
import random
from game import ASSET_DIR, MAP_ASSET_DIR, CHARACTER_ASSET_DIR
from .abstracts import CharacterAbstract

STATS_FONT = pygame.font.SysFont("comicsans", 17)

class Character(CharacterAbstract):
    """The character class for the game"""
    
    MAX_ROTATION = 25 # The maximum rotation of the character
    ROT_VEL = 1 # The rotation velocity
    ANIMATION_TIME = 4 # The time for the animation
    VEL = 5 # Default velocity
    NAME = "Character"
    images = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.IMGS = self.load_images()
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0 # velocity
        self.height = self.y
        self.img_count = 0 # Keeps track of the current image being displayed
        self.img = self.IMGS[0] # Current image being displayed

    def load_images(self):
        """Loads the images of the character"""
        # Checks if the images is not empty
        if not self.images:
            raise ValueError("The images property must not be empty")
        return [pygame.transform.scale2x(pygame.image.load(os.path.join(CHARACTER_ASSET_DIR, self.images[i]))) for i in range(len(self.images))]
        
    
    def jump(self):
        """The jump method of the character"""
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """Manages the movement of the character"""
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.4*self.tick_count**2 # how much the bird moves up or down 

        if d >= 14: # terminal velocity
            d = 14 # if the bird is moving down faster than 14 pixels, it will not move faster than 16 pixels

        if d < 0: # if the bird is moving up, it will move up a little bit more
            d -= 2
        self.y = self.y + d

        if d < 13:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -50 and self.tick_count > 10:
                self.tilt -= self.ROT_VEL/1.3

    def draw(self, win):
        """Manages the animation of the sprites"""
        self.img_count += 1 # Increments the image count every time the draw method is called

        self.img = self.IMGS[self.img_count // self.ANIMATION_TIME % self._image_count] # Divides the tick count by the animation time and gets the remainder to get the index of the image to display
        # Think of the `self.img_count` as the time then you will divide the time by the animation time to get the remainder which will be the index of the image to display
        
        # Computes the frames per animation
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # This renders the name over the head of the character
        #name = STATS_FONT.render(self.NAME, 1, (255, 255, 255))
        # parameter contains the name of the character, anti-aliasing value, and the color of the font by RGB values
        # NOTICE: Font will need to be changed
        # Code below will render the name of the character over the head of the character
        #win.blit(name, (self.x + 10, self.y - 40)) # Renders it above and center of the character.
        
        # Rotates the image of the character by the tilt value
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center) # Rotates the image of the character by the tilt value
        
        win.blit(rotated_image, new_rect.topleft) # Draws the image of the character on the window

    def get_mask(self):
        """Returns the mask of the character"""
        return pygame.mask.from_surface(self.img)
    
    @property
    def _image_count(self):
        """Returns the number of images in the sprite list"""
        return len(self.IMGS)

class Pipe:
    """The pipe class for the game"""
    
    # Generate pipe gaps based on a range
    GAP = random.randrange(220,280)

    VEL = 5
    """The velocity of the pipe"""

    def __init__(self, x, img):
        self.x = x # The x position of the pipe
        self.height = 0 # The height of the pipe
        self.top = 0 # The top of the pipe
        self.bottom = 0 # The bottom of the pipe

        self.PIPE_TOP = pygame.transform.flip(img, False, True) # Flips the image of the pipe from the bottom to the top
        self.PIPE_BOTTOM = img # The bottom pipe

        self.passed = False # If the bird has passed the pipe
        self.set_height() # Sets the height of the pipe

    def set_height(self):
        """Sets the height of the pipe"""
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """Moves the pipe to the left"""
        self.x -= self.VEL
    
    def draw(self, win):
        """Draws the pipe on the window"""
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird):
        """Returns True if a collision occurs
        
        Everytime the bird moves, the mask of the bird is updated and the mask of the pipes is also updated and check if its collided with the bird
        """
        bird_mask = bird.get_mask() # Gets the mask of the bird or the pixels that are not transparent
        # Mask of the pipes
        top_mask = pygame.mask.from_surface(self.PIPE_TOP) # Gets the mask of the top pipe
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM) # Gets the mask of the bottom pipe

        top_offset = (self.x - bird.x, self.top - round(bird.y)) # Gets the offset of the top pipe
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y)) # Gets the offset of the bottom pipe
        # Point of collision
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # Returns the point of collision between the bird and the bottom pipe
        t_point = bird_mask.overlap(top_mask, top_offset)    # Returns the point of collision between the bird and the top pipe

        if t_point or b_point: # If the bird collides with the top or bottom pipe
            return True

        return False
    
    def create_clone(self, x):
        """Creates a new instance of the pipe"""
        # Returns a new instance of the pipe with same parameters
        return self.__class__(self.x + x, self.PIPE_BOTTOM)
    
class Base:
    """ The base class for the floor and the background of the game """
    VEL = 5 # default velocity
    WIDTH = None
    IMG = None

    def __init__(self, y, base, velocity = None):
        self.IMG = base
        self.WIDTH = self.IMG.get_width()
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        
        if velocity != None:
            self.VEL = velocity
        
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

class Floor(Base):
    """The floor of the game"""
    VEL = 5 # default velocity
    """The velocity of the floor movement from right to left"""

    def __init__(self, y, base , velocity = None):
        super().__init__(y, base, velocity)
        self.VEL = velocity if velocity else self.VAL
    
    def collide(self, bird):
        """Returns True if the bird has collided with the floor"""
        if bird.y + bird.img.get_height() >= self.y:
            return True
        return False

# class Background(Base):
#     """The background of the game
    
#     This is not integrated yet need to modify to use the animation brackground
#     """
#     VEL = 5

#     def __init__(self, y, bg, velocity = None):
#         super().__init__(y, bg, velocity)
#         self.VEL = velocity if velocity else self.VEL
