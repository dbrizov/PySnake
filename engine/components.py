import pygame
from engine.vector import Vector2
from engine.color import Color
from engine.screen import Screen
from engine.input import Input
from engine.input import InputEvent


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

    def tick(self, deltaTime):
        pass

    def getEntity(self):
        return self._entity


class TransformComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self._priority = ComponentPriority.TRANSFORM_COMPONENT
        self.position = Vector2.ZERO


class RenderComponent(Component):
    def __init__(self, surfaceSize: Vector2):
        Component.__init__(self)
        self._priority = ComponentPriority.RENDER_COMPONENT
        self._surface = pygame.Surface(surfaceSize, pygame.SRCALPHA, 32)

    def tick(self, deltaTime):
        raise NotImplementedError("RenderComponent is abstract")


class RectRenderComponent(RenderComponent):
    def __init__(self, surfaceSize: Vector2, rectSize: Vector2, color: Color, posOffset=Vector2.ZERO, border=0):
        RenderComponent.__init__(self, surfaceSize)
        self.rectSize = rectSize
        self.color = color
        self.posOffset = posOffset
        self.border = border

    def tick(self, deltaTime):
        pygame.draw.rect(
            self._surface,
            self.color,
            (self.posOffset.x, self.posOffset.y, self.rectSize.x, self.rectSize.y),
            self.border)
        Screen.getSurface().blit(self._surface, self.getEntity().getTransform().position)


class TextRenderComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self._priority = ComponentPriority.RENDER_COMPONENT
        self._fontSize = 20
        self._fontName = "mono"
        self._font = pygame.font.SysFont(self._fontName, self._fontSize)
        self._bold = False
        self._text = ""
        self._color = Color.WHITE

    def tick(self, deltaTime):
        Component.tick(self, deltaTime)
        self.drawText_Internal()

    def getFontSize(self):
        return self._fontSize

    def setFontSize(self, fontSize):
        self._fontSize = fontSize
        self._font = pygame.font.SysFont(self._fontName, self._fontSize, self._bold)

    def getFontName(self):
        return self._fontName

    def setFontName(self, fontName):
        self._fontName = fontName
        self._font = pygame.font.SysFont(self._fontName, self._fontSize, self._bold)

    def isBold(self):
        return self._bold

    def setBold(self, bold):
        self._bold = bold
        self._font = pygame.font.SysFont(self._fontName, self._fontSize, self._bold)

    def getText(self):
        return self._text

    def setText(self, text):
        self._text = text

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color

    def getRectSize(self):
        width, height = self._font.size(self._text)
        return Vector2(width, height)

    def drawText_Internal(self):
        surface = self._font.render(self._text, True, self._color)
        Screen.getSurface().blit(surface, self.getEntity().getTransform().position)


class InputComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self._priority = ComponentPriority.INPUT_COMPONENT
        self._boundFunctionsByAxis = dict()
        self._boundFunctionsByPressedAction = dict()
        self._boundFunctionsByReleasedAction = dict()

    def enterPlay(self):
        Component.enterPlay(self)
        Input.onInputEvent += self.onInputEvent_Internal

    def exitPlay(self):
        Component.exitPlay(self)
        Input.onInputEvent -= self.onInputEvent_Internal

    def bindAxis(self, axisName, function):
        if (axisName not in self._boundFunctionsByAxis):
            self._boundFunctionsByAxis[axisName] = list()
        self._boundFunctionsByAxis[axisName].append(function)

    def unbindAxis(self, axisName, function):
        self._boundFunctionsByAxis[axisName].remove(function)

    def bindAction(self, actionName, eventType, function):
        if (eventType == InputEvent.EVENT_TYPE_PRESSED):
            if (actionName not in self._boundFunctionsByPressedAction):
                self._boundFunctionsByPressedAction[actionName] = list()
            self._boundFunctionsByPressedAction[actionName].append(function)
        elif (eventType == InputEvent.EVENT_TYPE_RELEASED):
            if (actionName not in self._boundFunctionsByReleasedAction):
                self._boundFunctionsByReleasedAction[actionName] = list()
            self._boundFunctionsByReleasedAction[actionName].append(function)

    def unbindAction(self, actionName, eventType, function):
        if (eventType == InputEvent.EVENT_TYPE_PRESSED):
            self._boundFunctionsByPressedAction[actionName].remove(function)
        elif (eventType == InputEvent.EVENT_TYPE_RELEASED):
            self._boundFunctionsByReleasedAction[actionName].remove(function)

    def clearBindings(self):
        self._boundFunctionsByAxis.clear()
        self._boundFunctionsByPressedAction.clear()
        self._boundFunctionsByReleasedAction.clear()

    def onInputEvent_Internal(self, inputEvent):
        if (inputEvent.type == InputEvent.EVENT_TYPE_AXIS):
            if (inputEvent.name in self._boundFunctionsByAxis):
                for func in self._boundFunctionsByAxis[inputEvent.name]:
                    func(inputEvent.axisValue)
        elif (inputEvent.type == InputEvent.EVENT_TYPE_PRESSED):
            if (inputEvent.name in self._boundFunctionsByPressedAction):
                for func in self._boundFunctionsByPressedAction[inputEvent.name]:
                    func()
        elif (inputEvent.type == InputEvent.EVENT_TYPE_RELEASED):
            if (inputEvent.name in self._boundFunctionsByReleasedAction):
                for func in self._boundFunctionsByReleasedAction[inputEvent.name]:
                    func()
