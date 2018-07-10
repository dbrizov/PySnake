import pygame
from engine.screen import Screen
from engine.gameloop import GameLoop
from engine.entity import EntitySpawner
from engine.components import RenderComponent
from engine.vector import Vector2
from engine.color import Color


def main():
    pygame.init()
    Screen.init(width=960, height=720, flags=pygame.DOUBLEBUF)

    render_component = RenderComponent(parent_surface=Screen.get_surface(), surface_width=50, surface_height=50, surface_color=Color.GREEN)
    entity = EntitySpawner.spawn_entity([render_component])
    entity.get_transform().position = Vector2(50, 50)

    GameLoop(fps=60).run()
    pygame.quit()


if (__name__ == "__main__"):
    main()
