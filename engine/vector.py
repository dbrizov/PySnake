import math


class Vector2(tuple):
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __add__(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector):
        return Vector2(self.x - vector.x, self.y - vector.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "({0:.2f}, {1:.2f})".format(self.x, self.y)

    @property
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    @property
    def magnitude_sqr(self):
        return self.x * self.x + self.y * self.y

    @property
    def normalized(self):
        return Vector2(self.x / self.magnitude, self.y / self.magnitude)


Vector2.ZERO = Vector2(0, 0)
