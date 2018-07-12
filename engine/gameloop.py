import pygame
from engine.time import Time
from engine.screen import Screen
from engine.entity import EntitySpawner


class GameLoop(object):
    def __init__(self, fps=60):
        Time.set_fps(fps)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            Time._tick()

            EntitySpawner._resolve_entity_spawn_requests()
            EntitySpawner._resolve_entity_destroy_requests()

            for entity in EntitySpawner.get_entities():
                entity.tick(Time.get_delta_time())

            Screen.repaint()
