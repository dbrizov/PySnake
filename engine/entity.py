from engine.components import TransformComponent
from sortedcontainers import SortedList
from sortedcontainers import SortedSet


class Entity:
    def __init__(self, priority, initialComponents):
        """
        `priority` -> `enterPlay()`, `exitPlay()` and `tick()` are called for every entity.
        The `priority` indicated in which order the entities will be updated.
        If entity `A` has `priority=0`, and entity `B` has `priority=1`, `A` will be updated before `B`.
        *It cannot be changed at runtime*

        `initialComponents` -> the initial list of components that the entity has
        """
        self._priority = priority
        self._transform = TransformComponent()
        self._components = SortedList(iterable=[self._transform], key=(lambda comp: comp._priority))
        if (initialComponents is not None):
            self._components.update(initialComponents)

    def init(self):
        for comp in self._components:
            comp.init(self)

    def enterPlay(self):
        for comp in self._components:
            comp.enterPlay()

    def exitPlay(self):
        for comp in self._components:
            comp.exitPlay()

    def tick(self, deltaTime):
        for comp in self._components:
            comp.tick(deltaTime)

    def getTransform(self):
        return self._transform

    def addComponent(self, component):
        self._components.add(component)

    def removeComponent(self, component):
        self._components.remove(component)

    def getComponent(self, classObj):
        for comp in self._components:
            if (isinstance(comp, classObj)):
                return comp
        return None


class EntitySpawner:
    _entities = SortedSet(key=(lambda entity: entity._priority))
    _entitySpawnRequests = SortedList(key=(lambda entity: entity._priority))
    _entityDestroyRequests = SortedList(key=(lambda entity: entity._priority))

    @staticmethod
    def getEntities():
        """Get all active entities"""
        return EntitySpawner._entities

    @staticmethod
    def spawnEntity(priority=0, initialComponents=None):
        """`entity.init()` is called immediatelly. `entity.enterPlay()` will be called on the next frame"""
        entity = Entity(priority, initialComponents)
        entity.init()
        EntitySpawner._entitySpawnRequests.add(entity)
        return entity

    @staticmethod
    def destroyEntity(entity):
        """`entity.exitPlay` will be called on the next frame"""
        EntitySpawner._entityDestroyRequests.add(entity)

    @staticmethod
    def resolveEntitySpawnRequests_Internal():
        for entity in EntitySpawner._entitySpawnRequests:
            EntitySpawner._entities.add(entity)
            entity.enterPlay()

        EntitySpawner._entitySpawnRequests.clear()

    @staticmethod
    def resolveEntityDestroyRequests_Internal():
        for entity in EntitySpawner._entityDestroyRequests:
            EntitySpawner._entities.remove(entity)
            entity.exitPlay()

        EntitySpawner._entityDestroyRequests.clear()
