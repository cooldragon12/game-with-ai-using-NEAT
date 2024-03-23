import os

ASSET_DIR =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

CHARACTER_ASSET_DIR = os.path.join(ASSET_DIR, "character")
MAP_ASSET_DIR = os.path.join(ASSET_DIR, "map")

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
TICK_RATE = 30