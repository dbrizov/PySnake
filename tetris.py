import pygame
from engine.screen import Screen
from engine.gameloop import GameLoop
from engine.entity import EntitySpawner
from engine.components import RectRenderComponent
from engine.vector import Vector2
from engine.color import Color


def main():
    pygame.init()
    Screen.init(width=960, height=720, flags=0, depth=32)

    background_renderer = RectRenderComponent(Vector2(Screen.get_width(), Screen.get_height()), Color(0, 0, 0))
    EntitySpawner.spawn_entity(priority=0, list_of_components=[background_renderer])

    rect_renderer = RectRenderComponent(Vector2(50, 50), Color(255, 0, 0))
    entity = EntitySpawner.spawn_entity(priority=0, list_of_components=[rect_renderer])
    entity.get_transform().position = Vector2(0, 0)

    GameLoop(fps=60).run()
    pygame.quit()


if (__name__ == "__main__"):
    main()
