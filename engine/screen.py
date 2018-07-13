import pygame.display


class Screen:
    _surface = None

    @staticmethod
    def init(width, height, flags=0, depth=0):
        Screen._surface = pygame.display.set_mode((width, height), flags, depth)

    @staticmethod
    def repaint():
        pygame.display.flip()

    @staticmethod
    def getSurface():
        return Screen._surface

    @staticmethod
    def getSize():
        return Screen._surface.get_size()

    @staticmethod
    def getWidth():
        return Screen._surface.get_width()

    @staticmethod
    def getHeight():
        return Screen._surface.get_height()
