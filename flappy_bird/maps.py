# Maps that will be used in the game is put in this file
# Use the Map Class to inherit in different maps
# The Map class will handle the movement of the pipes, the ground and background images, also the game play

from hmac import new
import random
import os
from re import M
import pygame

from .objects import Pipe, Floor
from game import MAP_ASSET_DIR
class MapAbstract:
    """MapAbstract class will handle"""
    currentInstances = 0
    maxInstances = 1
    
    def __new__(cls):
        if cls.currentInstances >= cls.maxInstances:
            raise ValueError(f'You can only make {cls.maxInstances} instances.')

        cls.currentInstances += 1
        return super().__new__(cls)
    
class Map:
    """Map Class handles the movement of the pipes, the ground and background images, also the game play
    
    Base class for the maps in the game
        """
    name = "Default"
    pipe = Pipe(600, pygame.transform.scale2x(pygame.image.load(os.path.join(MAP_ASSET_DIR, "default\\pipe.png"))))
    floor = Floor(730, pygame.transform.scale2x(pygame.image.load(os.path.join(MAP_ASSET_DIR, "default\\base.png"))), velocity=6)
    bg = pygame.transform.scale2x(pygame.image.load(os.path.join(MAP_ASSET_DIR, "default\\bg.png")))
    pipes = [pipe]
    PIPE_GAP = 400
    @property
    def maps_available(self):
        return Map.__subclasses__()
    
    def __init__(self, pipe:Pipe=None, floor:Floor=None, bg=None):
        self.floor = floor if floor else self.floor
        self.bg = bg if bg else self.bg
        self.pipes = [pipe] if [pipe] else [self.pipe]

    def create_pipe(self):
        """Creates a new pipe instance and returns it with a different position"""
        return self.pipe.create_clone(self.PIPE_GAP)
    
class MapHandler(Map):
    """MapHandler class will handle the random generation of the pipes"""

    def new_map(self):
        # Generate a new map
        map_selected = random.choice(self.maps_available)()
        return map_selected
    
    def change_map(self,map):
        self.name = map.name
        self.pipe = map.pipe
        self.floor = map.floor
        self.bg = map.bg
        self.pipes = map.pipes
        return self

    def __init__(self):
        map_now = self.new_map()
        self.change_map(map_now)

    def __call__(self) -> Map:
        return self.map_now
    
    def __next__(self):
        return self.new_map()

# List here the maps that will be used in the game, inherit the Map class
class Map1(Map):
    """Map1 class will handle the first map"""
    def __init__(self):
        self.name = "Map1"
        self.pipe = Pipe(600, pygame.transform.scale2x(pygame.image.load(os.path.join(MAP_ASSET_DIR, "default\\pipe.png"))))
        self.floor = Floor(730, pygame.transform.scale2x(pygame.image.load(os.path.join(MAP_ASSET_DIR, "default\\base.png"))), velocity=6)
        self.bg = pygame.transform.scale((pygame.image.load(os.path.join(MAP_ASSET_DIR, "1\\bg.png"))), (288*2,512*1.7))
        self.pipes = [self.pipe]

class Map2(Map):
    """Map2 class will handle the second map"""
    def __init__(self):
        self.name = "Map2"
        self.pipe = Pipe(600, pygame.transform.scale2x(pygame.image.load(os.path.join(MAP_ASSET_DIR, "default\\pipe.png"))))
        self.floor = Floor(730, pygame.transform.scale2x(pygame.image.load(os.path.join(MAP_ASSET_DIR, "default\\base.png"))), velocity=6)
        self.bg = pygame.transform.scale2x(pygame.image.load(os.path.join(MAP_ASSET_DIR, "default\\bg.png")))
        self.pipes = [self.pipe]