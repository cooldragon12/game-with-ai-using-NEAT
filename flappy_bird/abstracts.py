from abc import ABCMeta, abstractmethod


class CharacterAbstract(metaclass=ABCMeta):
    """The abstract class for the characters in the game"""

    @property
    def images(self):
        """The images of the character"""
        raise NotImplementedError( "The images property must be implemented")

    @property
    def MAX_ROTATION(self):
        """The maximum rotation of the character"""
        raise NotImplementedError( "The MAX_ROTATION property must be implemented")

    @property
    def ROT_VEL(self):
        """The rotation velocity"""
        raise NotImplementedError( "The ROT_VEL property must be implemented")

    @property
    def ANIMATION_TIME(self):
        """The time for the animation"""
        raise NotImplementedError( "The ANIMATION_TIME property must be implemented")

    @property
    def NAME(self):
        """The name of the character"""
        raise NotImplementedError( "The NAME property must be implemented")

    @property
    def VEL(self):
        """The velocity of the character"""
        raise NotImplementedError( "The VEL property must be implemented")

    @abstractmethod
    def load_images(self):
        # Load the images of the character using the pygame.image.load
        # This will pass to the IMGS property as a list of images
        raise NotImplementedError( "The load_images method must be implemented")

    @abstractmethod
    def jump(self):
        # The jump method of the character
        raise NotImplementedError( "The jump method must be implemented")

class MapAbstract(metaclass=ABCMeta):
    """MapAbstract class will handle"""
    __currentInstances = 0
    __maxInstances = 1
    @property
    def name(self):
        """The name of the map"""
        raise NotImplementedError( "The name property must be implemented")

    @property
    def pipe(self):
        """The pipe of the map"""
        raise NotImplementedError( "The pipe property must be implemented")

    @property
    def floor(self):
        """The floor of the map"""
        raise NotImplementedError( "The floor property must be implemented")

    @property
    def bg(self):
        """The background of the map"""
        raise NotImplementedError( "The bg property must be implemented")

    @property
    def pipes(self):
        """The pipes of the map"""
        raise NotImplementedError( "The pipes property must be implemented")

    @property
    def PIPE_GAP(self):
        """The gap between the pipes"""
        raise NotImplementedError( "The PIPE_GAP property must be implemented")

    @property
    def PIPE_VEL(self):
        """The velocity of the pipes"""
        raise NotImplementedError( "The PIPE_VEL property must be implemented")
    
    @abstractmethod
    def create_pipe(self):
        """Creates a new pipe instance and returns it with a different position"""
        raise NotImplementedError( "The create_pipe method must be implemented")
    