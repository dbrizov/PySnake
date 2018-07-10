from pygame import Surface
from engine.vector import Vector2


class ComponentPriority:
    """Entities have components, and the components have a priority.
    This is the way that we define that component A must be updated before component B
    """
    PRIORITY_TRANSFORM_COMPONENT = 0
    PRIORITY_RENDER_COMPONENT = 100000


class Component(object):
    def __init__(self):
        self._priority = -1

    def init(self, entity):
        self._entity = entity

    def enter_play(self):
        pass

    def exit_play(self):
        pass

    def tick(self, delta_time):
        pass

    def get_entity(self):
        return self._entity


class TransformComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self._priority = ComponentPriority.PRIORITY_TRANSFORM_COMPONENT
        self.position = Vector2.ZERO


class RenderComponent(Component):
    def __init__(self, parent_surface, surface_width, surface_height, surface_color):
        Component.__init__(self)
        self._priority = ComponentPriority.PRIORITY_RENDER_COMPONENT
        self._parent_surface = parent_surface
        self._surface = Surface((surface_width, surface_height))
        self._surface.fill(surface_color)

    def tick(self, delta_time):
        pos = self.get_entity().get_transform().position
        self._parent_surface.blit(self._surface, pos)
