import pygame
from engine.screen import Screen
from engine.gameloop import GameLoop
from engine.entity import Entity
from engine.entity import EntitySpawner
from engine.components import RectRenderComponent
from engine.components import InputComponent
from engine.input import InputEvent
from engine.vector import Vector2
from engine.color import Color


def run():
    pygame.init()
    Screen.init(width=960, height=720, flags=0, depth=32)

    EntitySpawner.spawnEntity(Entity, initialComponents=[
        RectRenderComponent(Vector2(Screen.getWidth(), Screen.getHeight()), Color(0, 0, 0))
    ])

    rectEntity = EntitySpawner.spawnEntity(Entity, initialComponents=[
        RectRenderComponent(Vector2(50, 50), Color(255, 0, 0)),
        RectRenderComponent(Vector2(25, 25), Color(0, 255, 0)),
        RectRenderComponent(Vector2(12.5, 12.5), Color(0, 0, 255))
    ])

    inputComponent = rectEntity.addComponent(InputComponent())
    inputComponent.bindAction("left", InputEvent.EVENT_TYPE_PRESSED, (lambda: print("left pressed")))
    inputComponent.bindAction("left", InputEvent.EVENT_TYPE_RELEASED, (lambda: print("left released")))
    inputComponent.bindAction("right", InputEvent.EVENT_TYPE_PRESSED, (lambda: print("right pressed")))
    inputComponent.bindAction("right", InputEvent.EVENT_TYPE_RELEASED, (lambda: print("right released")))
    inputComponent.bindAction("up", InputEvent.EVENT_TYPE_PRESSED, (lambda: print("up pressed")))
    inputComponent.bindAction("up", InputEvent.EVENT_TYPE_RELEASED, (lambda: print("up released")))
    inputComponent.bindAction("down", InputEvent.EVENT_TYPE_PRESSED, (lambda: print("down pressed")))
    inputComponent.bindAction("down", InputEvent.EVENT_TYPE_RELEASED, (lambda: print("down released")))

    rectEntity.getTransform().position = Vector2(0, 0)

    GameLoop(fps=60).run()
    pygame.quit()
