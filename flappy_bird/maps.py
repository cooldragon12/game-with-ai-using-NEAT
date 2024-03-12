# Maps that will be used in the game is put in this file
# Use the Map Class to inherit in different maps
# The Map class will handle the movement of the pipes, the ground and background images, also the game play

import random
import os
import pygame

from .objects import Pipe, Floor
from .abstracts import MapAbstract
from game import MAP_ASSET_DIR

class Map(MapAbstract):
    """Map Class handles the movement of the pipes, the ground and background images, also the game play
    
    Base class for the maps in the game
        """
    name = "Default"
    pipe:Pipe = None
    floor:Floor = None
    bg = None
    pipes = []
    PIPE_GAP = 400
    PIPE_VEL = 5
    
    def __init__(self):
        self.load_assets()

    @property
    def maps_available(self):
        """Returns the available maps"""
        return Map.__subclasses__()

    def create_pipe(self):
        return self.pipes[0].create_clone(self.PIPE_GAP)
    
    def load_assets(self):
        """Loads the assets of the map"""
        self.pipes = [Pipe(600, pygame.transform.scale2x(pygame.image.load(os.path.join(MAP_ASSET_DIR, self.pipe))))]
        self.floor = Floor(730, pygame.transform.scale2x(pygame.image.load(os.path.join(MAP_ASSET_DIR, self.floor))), velocity=self.PIPE_VEL)
        self.bg = pygame.transform.scale2x(pygame.image.load(os.path.join(MAP_ASSET_DIR, self.bg)))

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
# class Map1(Map):
#     """Map1 class will handle the first map"""
    
#     name = "Map1"
#     pipe = "default\\pipe.png"
#     floor = "default\\floor.png"
#     bg = "default\\bg.png"
#     PIPE_VEL = 6
#     PIPE = 300

# class Map2(Map):
#     """Map2 class will handle the second map"""
#     name = "Map2"
#     pipe = "2\\pipe.png"
#     floor = "2\\floor.png"
#     bg = "2\\bg.png"
#     PIPE_VEL = 8
#     PIPE_GAP = 400

# class Map3(Map):
#     """Map3 class will handle the third map"""

#     name = "Map3"
#     pipe = "3\\pipe.png"
#     floor = "3\\floor.png"
#     bg = "3\\bg.png"
#     PIPE_VEL = 8
#     PIPE_GAP = 400


class Map4(Map):
    """Map4 class will handle the third map"""

    name = "Map4"
    pipe = "4\\pipe.png"
    floor = "4\\floor.png"
    bg = "4\\bg.png"
    PIPE_VEL = 8
    PIPE_GAP = 400
