# Maps that will be used in the game is put in this file
# Use the Map Class to inherit in different maps
# The Map class will handle the movement of the pipes, the ground and background images, also the game play

from .objects import Pipe, Floor
from typing import List


class Map:
    """Map Class handles the movement of the pipes, the ground and background images, also the game play
    
    Base class for the maps in the game
        """
    def __init__(self, pipes:List[Pipe], floor:Floor, bg):
        self.pipes = pipes
        self.floor = floor
        self.bg = bg

