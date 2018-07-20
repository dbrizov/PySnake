class Color(tuple):
    def __new__(cls, r, g, b, a=255):
        return tuple.__new__(cls, (r, g, b, a))

    @property
    def r(self):
        return self[0]

    @property
    def g(self):
        return self[1]

    @property
    def b(self):
        return self[2]

    @property
    def a(self):
        return self[3]

    def __add__(self, color):
        return Color(self.r + color.r, self.g + color.g, self.b + color.b, self.a + color.a)

    def __sub__(self, color):
        return Color(self.r - color.r, self.g - color.g, self.b - color.b, self.a - color.a)

    def __mul__(self, scalar):
        return Color(int(self.r * scalar), int(self.g * scalar), int(self.b * scalar), int(self.a * scalar))

    def __truediv__(self, scalar):
        return Color(int(self.r / scalar), int(self.g / scalar), int(self.b / scalar), int(self.a / scalar))

    def __str__(self):
        return "({0}, {1}, {2}, {3})".format(self.r, self.b, self.b, self.a)


Color.NONE = Color(0, 0, 0, 0)
Color.BLACK = Color(0, 0, 0)
Color.WHITE = Color(255, 255, 255)
Color.GRAY = Color(128, 128, 128)
Color.RED = Color(255, 0, 0)
Color.GREEN = Color(0, 255, 0)
Color.BLUE = Color(0, 0, 255)
Color.YELLOW = Color(255, 255, 0)
Color.MAGENTA = Color(255, 0, 255)
Color.CYAN = Color(0, 255, 255)
Color.ORANGE = Color(255, 165, 0)
