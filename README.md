# Flappy Tite - A Flappy Bird Clone with a NEAT AI

This is a simple clone of the popular mobile game Flappy Bird, made using the Pygame library. The game is controlled by a NEAT AI, which is a genetic algorithm that evolves a population of neural networks to play the game.

## Installation
Execute the following command to install the required packages:
```bash
pip install -r requirements.txt
```
NOTE: Use a python virtual environment to avoid conflicts with other packages.

## Usage
To run the game, execute the following command:
```bash
python main.py
```

## Folder Structure
### assets
Contains all the assets used in the game, such as images and sounds.

**character/** - Contains the images of the characters divided by the name of the character as folder.

**map/** - Contains the images of the maps divided by the name of the map as folder.

### flappy_bird
Contains the objects used in the game. Includes the behavior of the bird, the pipes, and the base.

### game
Contains the main game loop and the game logic.

## Main File
### main.py
Contains the driver code for the game. It initializes the game and runs the main game loop.

## Missing Features
Below is a list of features that are missing from the game:
- [] Collision functionality
- [] Game Over functionality

Note: Changes to the game are welcome. Please create a pull request with the changes you want to make.