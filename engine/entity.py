from engine.components import TransformComponent
from sortedcontainers import SortedList
from sortedcontainers import SortedSet


class Entity:
    def __init__(self, priority, list_of_components):
        """
        `priority` -> `enter_play()`, `exit_play()` and `tick()` are called for every entity.
        The `priority` indicated in which order the entities will be updated.
        If entity `A` has `priority=0`, and entity `B` has `priority=1`, `A` will be updated before `B`.
        *It cannot be changed at runtime*

        `list_of_components` -> the initial list of components that the entity has
        """
        self._priority = priority
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
    _entities = SortedSet(key=(lambda entity: entity._priority))
    _entity_spawn_requests = SortedList(key=(lambda entity: entity._priority))
    _entity_destroy_requests = SortedList(key=(lambda entity: entity._priority))

    @staticmethod
    def get_entities():
        """Get all active entities"""
        return EntitySpawner._entities

    @staticmethod
    def spawn_entity(priority=0, list_of_components=None):
        """`entity.init()` is called immediatelly. `entity.enter_play()` will be called on the next frame"""
        entity = Entity(priority, list_of_components)
        entity.init()
        EntitySpawner._entity_spawn_requests.add(entity)
        return entity

    @staticmethod
    def destroy_entity(entity):
        """`entity.exit_play` will be called on the next frame"""
        EntitySpawner._entity_destroy_requests.add(entity)

    @staticmethod
    def _resolve_entity_spawn_requests():
        for entity in EntitySpawner._entity_spawn_requests:
            EntitySpawner._entities.add(entity)
            entity.enter_play()

        EntitySpawner._entity_spawn_requests.clear()

    @staticmethod
    def _resolve_entity_destroy_requests():
        for entity in EntitySpawner._entity_destroy_requests:
            EntitySpawner._entities.remove(entity)
            entity.exit_play()

        EntitySpawner._entity_destroy_requests.clear()
