"""This module contains the classes for the characters in the game."""

# The characters might change depending to the designer hahahhaha

from .objects import Character

# class Cat(Character):
#     # Sample character 
#     # MAX_ROTATION = 25
#     # ROT_VEL = 20
#     # ANIMATION_TIME = 4
#     # VEL = 5
#     # NAME = "Cat"
#     # images = ["char_folder_name\\char1.png", "char_folder_name\\char2.png", "char_folder_name\\char3.png]
#     pass

class Bird(Character):
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 4
    VEL = 5
    NAME = "Birdy"
    images = ["bird\\bird1.png", "bird\\bird2.png", "bird\\bird3.png"]

class Cat(Character):
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 1
    VEL = 5
    NAME = "PussyCat"
    images = ["cat\\cat1.png", "cat\\cat2.png", "cat\\cat3.png"]

class Racoon(Character):
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 2
    VEL = 5
    NAME = "Thiefy"
    images = ["racoon\\racoon1.png", "racoon\\racoon2.png", "racoon\\racoon3.png"]

class Bunny(Character):
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 4
    VEL = 5
    NAME = "Glowy"
    images = ["bunny\\bunny1.png", "bunny\\bunny1.png"]

class Duck(Character):
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 4
    VEL = 5
    NAME = "Key"
    images = ["duck\\duck1.png", "duck\\duck2.png", "duck\\duck3.png"]

class Fish(Character):
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 4
    VEL = 5
    NAME = "Nemo"
    images = ["fish\\fish1.png", "fish\\fish2.png", "fish\\fish3.png"]

class Ghost(Character):
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 4
    VEL = 5
    NAME = "Naghost"
    images = ["ghost\\ghost1.png", "ghost\\ghost1.png"]