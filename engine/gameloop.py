import pygame
from engine.time import Time
from engine.screen import Screen
from engine.entity import EntitySpawner
from engine.input import Input


class GameLoop(object):
    def __init__(self, fps=60):
        Time.setFps(fps)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            Time.tick_Internal()
            Input.tick_Internal(Time.getDeltaTime())

            EntitySpawner.resolveEntitySpawnRequests_Internal()
            EntitySpawner.resolveEntityDestroyRequests_Internal()

            for entity in EntitySpawner.getEntities():
                entity.tick(Time.getDeltaTime())

            Screen.repaint()
