import pygame
from engine.screen import Screen
from engine.gameloop import GameLoop


def main():
    pygame.init()
    Screen.init(width=960, height=720, flags=pygame.DOUBLEBUF)
    GameLoop(fps=60).run()
    pygame.quit()


if (__name__ == "__main__"):
    main()
