"""This module contains the classes for the characters in the game."""

# The characters might change depending to the designer hahahhaha

from .objects import Character

# Example:
# class CharacterName(Character):
#     # Sample character 
#     MAX_ROTATION = 25 # The maximum rotation of the character
#     ROT_VEL = 20    # The rotation velocity
#     ANIMATION_TIME = 4 # The time for the animation
#     VEL = 5
#     NAME = "name of the character"
#     images = ["char_folder_name\\char1.png", "char_folder_name\\char2.png", "char_folder_name\\char3.png]
#     

class Whale(Character):
    pass

class Bird(Character):
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 4
    VEL = 5
    NAME = "Birdy"
    images = ["bird\\bird1.png", "bird\\bird2.png", "bird\\bird3.png"]

class Jellyfish(Character):
    pass

class Duck(Character):
    pass

class Fish(Character):
    pass

class Ghost(Character):
    pass