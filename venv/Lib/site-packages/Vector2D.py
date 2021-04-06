#/usr/bin/pythonw

import math

class Vector2D(object):

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return ('({}, {})'.format(self.x, self.y))

    @classmethod
    def vector_from_points(cls, P1, P2):
        return cls(P2[0] - P1[0], P2[1] - P1[1])

    def get_magnitude(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))

    def normalize(self):
        magnitude = self.get_magnitude()
        self.x /= magnitude
        self.y /= magnitude

    def __add__(self, anv):
        return Vector2D(self.x + anv.x, self.y + anv.y)

    def __sub__(self, anv):
        return Vector2D(self.x - anv.x, self.y - anv.y)

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)
        
    def __iter__(self):
        return [self.x, self.y].__iter__()
    
        
