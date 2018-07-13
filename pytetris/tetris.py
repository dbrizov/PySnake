import pygame
from engine.screen import Screen
from engine.gameloop import GameLoop
from engine.entity import EntitySpawner
from engine.components import RectRenderComponent
from engine.vector import Vector2
from engine.color import Color


def run():
    pygame.init()
    Screen.init(width=960, height=720, flags=0, depth=32)

    backgroundRenderer = RectRenderComponent(Vector2(Screen.getWidth(), Screen.getHeight()), Color(0, 0, 0))
    EntitySpawner.spawnEntity(priority=0, initialComponents=[backgroundRenderer])

    rectRenderer = RectRenderComponent(Vector2(50, 50), Color(255, 0, 0))
    entity = EntitySpawner.spawnEntity(priority=0, initialComponents=[rectRenderer])
    entity.getTransform().position = Vector2(0, 0)

    GameLoop(fps=60).run()
    pygame.quit()
