from __future__ import division

import math
import random

# A kick-ass 2D vector class.
class Vector(object):

    # Factory Methods {{{1
    @staticmethod
    def null():
        return Vector(0, 0)

    @staticmethod
    def random():
        theta = random.uniform(0, 2 * math.pi)
        return Vector(math.cos(theta), math.sin(theta))

    @staticmethod
    def from_radians(angle):
        return Vector(math.cos(angle), math.sin(angle))

    @staticmethod
    def from_degrees(angle):
        return Vector.from_radians(angle * math.pi / 180)

    # Math Methods {{{1
    @staticmethod
    def get_radians(A, B):
        try:
            temp = A.get_magnitude() * B.get_magnitude()
            temp = Vector.dot(A, B) / temp
            return math.acos(temp)

        # Floating point error will confuse the trig functions occasionally.
        except ValueError:
            return 0 if temp > 0 else pi

        # It doesn't make sense to find the angle of a null vector. 
        except ZeroDivisionError:
            raise NullVectorError()

    @staticmethod
    def get_degrees(A, B):
        return Vector.get_radians(A, B) * 180 / math.pi

    @staticmethod
    def get_distance(A, B):
        return (A - B).get_magnitude()

    @staticmethod
    def get_manhattan(A, B):
        disp = B - A
        return abs(disp.x) + abs(disp.y)

    @staticmethod
    def dot_product(A, B):
        return A.x * B.x + A.y * B.y

    @staticmethod
    def perp_product(A, B):
        # This is just a cross product where the third dimension is zero.
        return A.x * B.y - A.y * B.x

    dot = dot_product
    perp = perp_product
    # }}}1

    # Operators {{{1
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __iter__(self):
        yield self.x; yield self.y

    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector(self.x - v.x, self.y - v.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __abs__(self):
        return Vector(abs(self.x), abs(self.y))
    
    def __mul__(self, c):
        return Vector(c * self.x, c * self.y)

    def __rmul__(self, c):
        return Vector(c * self.x, c * self.y)

    def __div__(self, c):
        return Vector(self.x / float(c), self.y / float(c))

    def __truediv__(self, c):
        return Vector(self.x / c, self.y / c)

    def __floordiv__(self, c):
        return Vector(self.x // c, self.y // c)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __nonzero__(self):
        return self.x != 0 or self.y != 0

    def __repr__(self):
        return "<%f, %f>" % self.get_tuple()

    def __str__(self):
        return self.__repr__()

    # Attributes {{{1
    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def r(self):
        return self.__x
    
    @property
    def th(self):
        return self.__y

    @property
    def tuple(self):
        return self.x, self.y

    @property
    def pygame(self):
        return int(self.x), int(self.y)

    @property
    def magnitude(self):
        return math.sqrt(self.magnitude_squared)

    @property
    def magnitude_squared(self):
        return self.x**2 + self.y**2

    @property
    def normal(self):
        try:
            return self / self.magnitude
        except ZeroDivisionError:
            raise NullVectorError()

    @property
    def orthogonal(self):
        return Vector(-self.y, self.x)

    @property
    def orthonormal(self):
        return self.orthogonal.normal

    @property
    def components(self, v):
        tangent = v * Vector.dot(self, v)
        normal = self - tangent
        return normal, tangent

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_r(self):
        return self.r

    def get_th(self):
        return self.th

    def get_tuple(self):
        return self.tuple

    def get_pygame(self):
        return self.pygame

    def get_magnitude(self):
        return self.magnitude

    def get_magnitude_squared(self):
        return self.magnitude_squared

    def get_normal(self, magnitude=1):
        return magnitude * self.normal

    def get_orthogonal(self):
        return self.orthogonal

    def get_orthonormal(self, magnitude=1):
        return magnitude * self.orthonormal

    def get_components(self, v):
        return self.components
    # }}}1

class NullVectorError(Exception):
    pass

if __name__ == "__main__":

    def factory_tests():
        """ Make sure that the factory methods return the right objects. """

        assert Vector.null() == Vector(0, 0)

        degrees = (0, 90, 180, 270)
        radians = (0, math.pi / 2, math.pi, 3 * math.pi / 2)

        for d, r in zip(degrees, radians):
            assert Vector.from_radians(r) == Vector.from_degrees(d)

    def math_tests():
        """ Make sure that the mathematical utilities return the correct
        answers.  In particular, make sure that they can all cope with
        degenerate input. """


    print "Testing vector.py..."

    factory_tests()

    print "All tests passed."
    print "However, there are not many tests for this module.  Use with caution."
