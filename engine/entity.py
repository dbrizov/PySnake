from engine.components import TransformComponent
from sortedcontainers import SortedList


class Entity:
    def __init__(self, list_of_components=None):
        self._transform = TransformComponent()
        self._components = SortedList(iterable=[self._transform], key=(lambda comp: comp._priority))
        if (list_of_components is not None):
            self._components.update(list_of_components)

    def init(self):
        for comp in self._components:
            comp.init(self)

    def enter_play(self):
        for comp in self._components:
            comp.enter_play()

    def exit_play(self):
        for comp in self._components:
            comp.exit_play()

    def tick(self, delta_time):
        for comp in self._components:
            comp.tick(delta_time)

    def get_transform(self):
        return self._transform

    def add_component(self, component):
        self._components.add(component)

    def remove_component(self, component):
        self._components.remove(component)

    def get_component(self, class_obj):
        for comp in self._components:
            if (isinstance(comp, class_obj)):
                return comp
        return None


class EntitySpawner:
    _entities = set()

    @staticmethod
    def get_entities():
        return EntitySpawner._entities

    @staticmethod
    def spawn_entity(list_of_components):
        entity = Entity(list_of_components)
        entity.init()
        entity.enter_play()
        EntitySpawner._entities.add(entity)
        return entity

    @staticmethod
    def destroy_entity(entity):
        entity.exit_play()
        EntitySpawner._entities.remove(entity)
