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
    pipe: Pipe = None
    floor: Floor = None
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
        self.pipes = [
            Pipe(
                600,
                pygame.transform.scale(
                    pygame.image.load(os.path.join(MAP_ASSET_DIR, self.pipe)),
                    (52 * 2, 329 * 2),
                ),
            )
        ]
        self.floor = Floor(
            730,
            pygame.transform.scale(
                pygame.image.load(os.path.join(MAP_ASSET_DIR, self.floor)),
                (350 * 2, 112 * 2.2),
            ),
            velocity=self.PIPE_VEL,
        )
        self.bg = pygame.transform.scale(
            pygame.image.load(os.path.join(MAP_ASSET_DIR, self.bg)),
            (300 * 2, 515 * 1.5),
        )


class MapHandler(Map):
    """MapHandler class will handle the random generation of the pipes"""

    def new_map(self):
        # Generate a new map
        map_selected = random.choice(self.maps_available)()  # Randomly selects a map
        return map_selected

    def change_map(self, map):
        # Change the map
        self.name = map.name
        self.pipe = map.pipe
        self.floor = map.floor
        self.bg = map.bg
        self.pipes = map.pipes
        return self

    def __init__(self):
        map_now = self.new_map()  # Generates a new map upon initialization
        self.change_map(map_now)  # Applying the new map

    def __call__(self) -> Map:
        return self.map_now  # Returns the current map

    def __next__(self):
        return self.new_map()


# List here the maps that will be used in the game, inherit the Map class
# class MapDefault(Map):
#     """MapDefault class will handle the first map"""

#     name = "MapDefault"
#     pipe = "default\\pipe.png"
#     floor = "default\\floor.png"
#     bg = "default\\bg.png"
#     PIPE_VEL = 6
#     PIPE_GAP = 400


# class MapFantasy(Map):
#     """MapFantasy class will handle map 1"""

#     name = "Fantasy"
#     pipe = "1\\pipe.png"
#     floor = "default\\floor.png"
#     bg = "1\\bg.png"
#     PIPE_VEL = 6
#     PIPE_GAP = 400


# class MapCity(Map):
#     """MapCity class will handle the map 2"""

#     name = "City"
#     pipe = "2\\pipe.png"
#     floor = "2\\floor.png"
#     bg = "2\\bg.png"
#     PIPE_VEL = 6
#     PIPE_GAP = 400


# class MapSnow(Map):
#     """MapSnow class will handle map 3"""

#     name = "Snow"
#     pipe = "3\\pipe.png"
#     floor = "3\\floor.png"
#     bg = "3\\bg.png"
#     PIPE_VEL = 6
#     PIPE_GAP = 400


# class MapNight(Map):
#     """MapNight class will handle map 4"""

#     name = "Night"
#     pipe = "4\\pipe.png"
#     floor = "4\\floor.png"
#     bg = "4\\bg.png"
#     PIPE_VEL = 6
#     PIPE_GAP = 200


# class MapWater(Map):
#     """MapWater class will handle map 5"""

#     name = "Water"
#     pipe = "5\\pipe.png"
#     floor = "5\\floor.png"
#     bg = "5\\bg.png"
#     PIPE_VEL = 6
#     PIPE_GAP = 400


class MapBatman(Map):
    """MapWater class will handle map 6"""

    name = "Batman"
    pipe = "6\\pipe.png"
    floor = "6\\floor.png"
    bg = "6\\bg.png"
    PIPE_VEL = 6
    PIPE_GAP = 400
