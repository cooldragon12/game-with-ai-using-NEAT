from .environment import Environment
import pygame
class TestAI(Environment):
    def controls(self, event):
        # Change this depending on the mode
        pass

    def collide_handler(self):
        pass

class Solo(Environment):
    pass

class AIvsPlayer(Environment):
    pass