from pygame import draw
from pygame import Surface
from engine.vector import Vector2
from engine.color import Color
from engine.screen import Screen


class ComponentPriority:
    INPUT_COMPONENT = -150
    TRANSFORM_COMPONENT = -100
    DEFAULT_COMPONENT = 0
    RENDER_COMPONENT = 100


class Component(object):
    def __init__(self):
        """The components in the `entity_component_list` of an `entity` are sorted by their `priority`.
        *The `priority` cannot be changed at runtime*
        """
        self._priority = ComponentPriority.DEFAULT_COMPONENT

    def init(self, entity):
        self._entity = entity

    def enterPlay(self):
        pass

    def exitPlay(self):
        pass

    def tick(self, delta_time):
        pass

    def getEntity(self):
        return self._entity


class TransformComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self._priority = ComponentPriority.TRANSFORM_COMPONENT
        self.position = Vector2.ZERO


class RenderComponent(Component):
    def __init__(self, size: Vector2, color: Color):
        Component.__init__(self)
        self._priority = ComponentPriority.RENDER_COMPONENT
        self._surface = Surface(size)
        self.color = color

    def tick(self, deltaTime):
        raise NotImplementedError("RenderComponent is abstract")


class RectRenderComponent(RenderComponent):
    def __init__(self, size: Vector2, color: Color):
        RenderComponent.__init__(self, size, color)
        self.size = size

    def tick(self, deltaTime):
        draw.rect(self._surface, self.color, (0, 0, self.size.x, self.size.y))
        Screen.getSurface().blit(self._surface, self.getEntity().getTransform().position)


class InputComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self._priority = ComponentPriority.INPUT_COMPONENT

    def tick(self, deltaTime):
        pass
