import pygame
import os
import random

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STATS_FONT = pygame.font.SysFont("comicsans", 50)

class Character:
    """The base class for the characters in the game"""
    IMGS = None
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 4
    
    def __init__(self, x, y, loaded_character=BIRD_IMGS, name = "Birdy"):
        self.x = x
        self.y = y
        self.IMGS = loaded_character
        self.name = name
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2 # how much the bird moves up or down 

        if d >= 16: # terminal velocity
            d = 16 # if the bird is moving down faster than 16 pixels, it will not move faster than 16 pixels

        if d < 0: # if the bird is moving up, it will move up a little bit more
            d -= 2
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """Manages the animation of the sprites"""
        self.img_count += 1 # Increments the image count every time the draw method is called

        self.img = self.IMGS[self.img_count // self.ANIMATION_TIME % self._image_count] # Divides the tick count by the animation time and gets the remainder to get the index of the image to display
        # Computes the frames per animation
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
    @property
    def _image_count(self):
        """Returns the number of images in the sprite list"""
        return len(self.IMGS)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL
    
    def draw(self, win):
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
    
class Base:
    VEL = 5 # default velocity
    WIDTH = None
    IMG = None

    def __init__(self, y, base = BASE_IMG, velocity = None):
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
    VAL = 5

    def __init__(self, y, base = BASE_IMG, velocity = None):
        super().__init__(y, base, velocity)
        self.VEL = self.VAL
    
    def collide(self, bird):
        if bird.y + bird.img.get_height() >= self.y or bird.y < 0:
            return True
        return False

class Background(Base):
    """The background of the game
    
    This is not integrated yet need to modify to use the animation brackground
    """
    VAL = 5

    def __init__(self, y, bg = BG_IMG, velocity = None):
        super().__init__(y, bg, velocity)
        self.VEL = self.VAL
