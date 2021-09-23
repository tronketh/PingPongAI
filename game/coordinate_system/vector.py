import math


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def project(self, angle: float, distance: float, copy=False):
        radians = math.radians(angle)
        x, y = self
        x += distance * math.cos(radians)
        y += distance * math.sin(radians)
        if copy:
            return Vector(x, y)
        else:
            self.x = x
            self.y = y

    def copy(self):
        return Vector(*self)

    def rotate(self, angle):
        radians = math.radians(angle)
        self.x = self.x * math.cos(radians) - self.y * math.sin(radians)
        self.y = self.x * math.sin(radians) + self.y * math.cos(radians)

    @staticmethod
    def x_distance(a, b):
        return abs(a.x - b.x)

    @staticmethod
    def y_distance(a, b, absolute=True):
        dist = a.y - b.y
        if absolute:
            return abs(a.y - b.y)
        return dist

    def __add__(self, other):
        x, y = other
        return Vector(self.x + x, self.y + y)

    def __sub__(self, other):
        x, y = other
        return Vector(self.x - x, self.y - y)

    def __str__(self):
        return f'Point({self.x}, {self.y})'

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        raise StopIteration

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        raise StopIteration
