import pygame
import weakref
import random
from collections import deque
from engine.vector import Vector2
from engine.color import Color
from engine.time import Time
from engine.screen import Screen
from engine.gameloop import GameLoop
from engine.entity import Entity
from engine.entity import EntitySpawner
from engine.components import RenderComponent
from engine.components import RectRenderComponent
from engine.components import TextRenderComponent
from engine.components import InputComponent
from engine.input import InputEvent
from engine.events import EventHook


DIRECTION_LEFT = Vector2(0, -1)
DIRECTION_RIGHT = Vector2(0, 1)
DIRECTION_UP = Vector2(-1, 0)
DIRECTION_DOWN = Vector2(1, 0)

CELL_SIZE = Vector2(20, 20)
CELL_BORDER_WIDTH = 2
CELL_TYPE_BLOCK = 1
CELL_TYPE_EMPTY = 0

CELL_MATRIX = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

CELL_MATRIX_2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class CellRenderComponent(RenderComponent):
    def __init__(self, surfaceSize, rectSize, borderWidth, fillColor, borderColor):
        RenderComponent.__init__(self, surfaceSize)
        self.rectSize = rectSize
        self.borderWidth = borderWidth
        self.fillColor = fillColor
        self.borderColor = borderColor

    def tick(self, deltaTime):
        pygame.draw.rect(self._surface, self.fillColor, (0, 0, self.rectSize.x, self.rectSize.y))
        pygame.draw.rect(self._surface, self.borderColor, (0, 0, self.rectSize.x, self.rectSize.y), self.borderWidth)
        Screen.getSurface().blit(
            self._surface,
            self.getEntity().getTransform().position + self.getEntity().getBoard().getTransform().position)


class CellEntity(Entity):
    def __init__(self, board, pos, type, priority=0, initialComponents=None):
        Entity.__init__(self, priority, initialComponents)
        self._board = weakref.ref(board)
        self._pos = pos
        self._type = type
        self.food = None

    def init(self):
        Entity.init(self)
        if (self._type == CELL_TYPE_EMPTY):
            self.addComponent(CellRenderComponent(CELL_SIZE, CELL_SIZE, CELL_BORDER_WIDTH, Color(25, 25, 25), Color.BLACK))
        if (self._type == CELL_TYPE_BLOCK):
            self.addComponent(CellRenderComponent(CELL_SIZE, CELL_SIZE, CELL_BORDER_WIDTH, Color.BLUE, Color.BLACK))

    def getBoard(self):
        return self._board()

    def getPos(self):
        return self._pos

    def getType(self):
        return self._type


class BoardEntity(Entity):
    def __init__(self, cellMatrix, priority=0, initialComponents=None):
        Entity.__init__(self, priority, initialComponents)
        self._cellMatrix = cellMatrix
        self._rows = len(self._cellMatrix)
        self._cols = len(self._cellMatrix[0])
        self._cells = list()

    def init(self):
        Entity.init(self)
        for row in range(self._rows):
            for col in range(self._cols):
                cellType = self._cellMatrix[row][col]
                cellEntity = EntitySpawner.spawnEntity(CellEntity, self, Vector2(row, col), cellType)
                cellEntity.getTransform().position = Vector2(col * CELL_SIZE.x, row * CELL_SIZE.y)
                self._cells.append(cellEntity)

    def getRows(self):
        return self._rows

    def getCols(self):
        return self._cols

    def getCell(self, row, col):
        return self._cells[self.getCellIndex_Internal(row, col)]

    def getCellIndex_Internal(self, row, col):
        return row * self._cols + col


class SnakeRenderComponent(RenderComponent):
    def __init__(self, surfaceSize, rectSize, borderWidth, bodyColor, borderColor):
        RenderComponent.__init__(self, surfaceSize)
        self.rectSize = rectSize
        self.borderWidth = borderWidth
        self.bodyColor = bodyColor
        self.borderColor = borderColor

    def tick(self, deltaTime):
        boardPos = self.getSnake().getBoard().getTransform().position
        self._surface.fill(Color.NONE)
        for pos in self.getSnake().getBodyPositions():
            rectPos = boardPos + Vector2(pos.y * self.rectSize.x, pos.x * self.rectSize.y)
            pygame.draw.rect(self._surface, self.bodyColor, (rectPos.x, rectPos.y, self.rectSize.x, self.rectSize.y))
            pygame.draw.rect(
                self._surface,
                self.borderColor,
                (rectPos.x, rectPos.y, self.rectSize.x, self.rectSize.y),
                self.borderWidth)

        Screen.getSurface().blit(self._surface, Vector2(0, 0))

    def getSnake(self):
        return self.getEntity()


class SnakeEntity(Entity):
    def __init__(self, board, speed, initialSize, initialHeadPos, initialDir, priority=0, initialComponents=None):
        Entity.__init__(self, priority, initialComponents)
        self._board = board
        self._headPos = initialHeadPos
        self._dir = initialDir
        self._deque = deque()
        for i in range(initialSize):
            self._deque.appendleft(initialHeadPos - initialDir * i)

        self._speed = speed
        self._passedDistance = 0.0
        self._dirQueue = deque()
        self._ateFood = False
        self.onFoodEaten = EventHook()

    def init(self):
        Entity.init(self)
        self._renderComponent = self.addComponent(
            SnakeRenderComponent(Screen.getSize(), CELL_SIZE, CELL_BORDER_WIDTH, Color.RED, Color.BLACK))

        self._inputComponent = self.addComponent(InputComponent())
        self._inputComponent.bindAction("left", InputEvent.EVENT_TYPE_PRESSED, lambda: self.changeDirection(DIRECTION_LEFT))
        self._inputComponent.bindAction("right", InputEvent.EVENT_TYPE_PRESSED, lambda: self.changeDirection(DIRECTION_RIGHT))
        self._inputComponent.bindAction("up", InputEvent.EVENT_TYPE_PRESSED, lambda: self.changeDirection(DIRECTION_UP))
        self._inputComponent.bindAction("down", InputEvent.EVENT_TYPE_PRESSED, lambda: self.changeDirection(DIRECTION_DOWN))

    def tick(self, deltaTime):
        Entity.tick(self, deltaTime)
        self._passedDistance += self._speed * deltaTime
        if (self._passedDistance > 1.0):
            self._passedDistance -= 1.0
            self.move_Internal()
            self.hangleCollisions_Internal()

    def getBoard(self):
        return self._board

    def getSpeed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def getHeadPos(self):
        return self._headPos

    def getNextHeadPos(self):
        return self._headPos + self._dir

    def getBodyPositions(self):
        return iter(self._deque)

    def changeDirection(self, newDir):
        length = len(self._dirQueue)
        if (length == 2):
            return

        lastQueueDir = self._dir
        if (length > 0):
            lastQueueDir = self._dirQueue[length - 1]
        if (newDir != lastQueueDir * -1.0):
            self._dirQueue.append(newDir)

    def move_Internal(self):
        if (self._ateFood):
            self._ateFood = False
        else:
            self._deque.popleft()

        if (len(self._dirQueue) > 0):
            self._dir = self._dirQueue.popleft()
        self._deque.append(self.getNextHeadPos())
        self._headPos = self.getNextHeadPos()

    def hangleCollisions_Internal(self):
        # Handle collision with block cells
        headCell = self._board.getCell(self._headPos.x, self._headPos.y)
        if (headCell.getType() == CELL_TYPE_BLOCK):
            EntitySpawner.destroyEntity(self)

        # Handle collision with itself
        bodyPositions = list(self.getBodyPositions())
        bodyPositions.remove(self._headPos)
        if (self._headPos in bodyPositions):
            EntitySpawner.destroyEntity(self)

        # Handle collision with food
        for cellPos in self.getBodyPositions():
            cell = self._board.getCell(cellPos.x, cellPos.y)
            if (cell.food is not None):
                self._ateFood = True
                food = cell.food
                cell.food = None
                EntitySpawner.destroyEntity(food)
                self.onFoodEaten.invoke()
                break

    def eatFood_Internal(self, cell, food):
        self._ateFood = True
        cell.food = None
        EntitySpawner.destroyEntity(food)
        self.onFoodEaten.invoke()


class FoodEntity(Entity):
    def __init__(self, board, pos, priority=0, initialComponents=None):
        Entity.__init__(self, priority, initialComponents)
        self._board = board
        self._pos = pos
        self.setPos(self._pos)
        self._board.getCell(self._pos.x, self._pos.y).food = self

    def init(self):
        Entity.init(self)
        self._renderComponent = self.addComponent(
            CellRenderComponent(CELL_SIZE, CELL_SIZE, CELL_BORDER_WIDTH, Color.GREEN, Color.BLACK))

    def getBoard(self):
        return self._board

    def getPos(self):
        return self._pos

    def setPos(self, pos):
        self._pos = pos
        self._transform.position = Vector2(pos.y * CELL_SIZE.x, pos.x * CELL_SIZE.y)


class GameControllerEntity(Entity):
    def init(self):
        Entity.init(self)
        self._inputComponent = self.addComponent(InputComponent())
        self._inputComponent.bindAction("pause", InputEvent.EVENT_TYPE_PRESSED, self.togglePaused)
        self._inputComponent.bindAction("cancel", InputEvent.EVENT_TYPE_PRESSED, self.quit)

        self._backgroundEntity = EntitySpawner.spawnEntity(Entity)
        self._backgroundEntity.addComponent(RectRenderComponent(Screen.getSize(), Screen.getSize(), Color.BLACK))

        self._boardEntity = EntitySpawner.spawnEntity(BoardEntity, CELL_MATRIX_2)

        self._snakeEntity = EntitySpawner.spawnEntity(SnakeEntity, self._boardEntity, 5, 3, Vector2(3, 3), DIRECTION_RIGHT)
        self._snakeEntity.onFoodEaten += lambda: self.spawnFood()
        self._snakeEntity.onFoodEaten += lambda: self.increaseScore()
        self._snakeEntity.onFoodEaten += lambda: self.increaseSnakeSpeed()
        self.spawnFood()

        self._pausedTextEntity = EntitySpawner.spawnEntity(Entity)
        self._pausedTextComp = self._pausedTextEntity.addComponent(TextRenderComponent())
        self._pausedTextComp.setFontName("mono")
        self._pausedTextComp.setFontSize(20)
        self._pausedTextComp.setBold(True)
        self._pausedTextComp.setColor(Color.WHITE)
        self._pausedTextComp.setText("PAUSED")
        pausedTextRectSize = self._pausedTextComp.getRectSize()
        boardRectSize = Vector2(self._boardEntity.getCols() * CELL_SIZE.x, self._boardEntity.getRows() * CELL_SIZE.y)
        self._pausedTextEntity.getTransform().position = Vector2((boardRectSize.x - pausedTextRectSize.x) // 2,
                                                                 (boardRectSize.y - pausedTextRectSize.y) // 2)

        self._scoreTextEntity = EntitySpawner.spawnEntity(Entity)
        self._scoreTextEntity.getTransform().position = Vector2(0, boardRectSize.y)
        self._scoreTextComp = self._scoreTextEntity.addComponent(TextRenderComponent())
        self._scoreTextComp.setFontName("mono")
        self._scoreTextComp.setFontSize(20)
        self._scoreTextComp.setBold(True)
        self._scoreTextComp.setColor(Color.WHITE)
        self._scoreTextComp.setText("SCORE:0")

        self._score = 0
        self._paused = True
        self.setPaused(True)

    def spawnFood(self):
        randRow = random.randrange(1, self._boardEntity.getRows() - 1)
        randCol = random.randrange(1, self._boardEntity.getCols() - 1)
        while (self._boardEntity.getCell(randRow, randCol).getType() == CELL_TYPE_BLOCK or
               Vector2(randRow, randCol) in self._snakeEntity.getBodyPositions()):
            randRow = random.randrange(1, self._boardEntity.getRows() - 1)
            randCol = random.randrange(1, self._boardEntity.getCols() - 1)

        EntitySpawner.spawnEntity(FoodEntity, self._boardEntity, Vector2(randRow, randCol))

    def increaseScore(self):
        self._score += 1
        self._scoreTextComp.setText("SCORE:{0}".format(self._score))

    def increaseSnakeSpeed(self):
        self._snakeEntity.setSpeed(self._snakeEntity.getSpeed() + 0.1)

    def setPaused(self, paused):
        self._paused = paused
        if (paused):
            Time.setTimeScale(0.0)
            self._pausedTextEntity.canTick = True
        else:
            Time.setTimeScale(1.0)
            self._pausedTextEntity.canTick = False

    def togglePaused(self):
        self.setPaused(not self._paused)

    def quit(self):
        pygame.quit()


def run():
    pygame.init()
    Screen.init(width=500, height=450, flags=0, depth=32)

    EntitySpawner.spawnEntity(GameControllerEntity)

    GameLoop(fps=60).run()
    pygame.quit()


if (__name__ == "__main__"):
    run()
