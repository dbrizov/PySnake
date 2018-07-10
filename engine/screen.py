import pygame.display


class Screen:
    _surface = None

    @staticmethod
    def init(width, height, flags=0, depth=0):
        Screen._surface = pygame.display.set_mode((width, height), flags, depth)

    @staticmethod
    def get_surface():
        return Screen._surface

    @staticmethod
    def get_size():
        return Screen._surface.get_size()

    @staticmethod
    def get_width():
        return Screen._surface.get_width()

    @staticmethod
    def get_height():
        return Screen._surface.get_height()
