from __future__ import division

from vector import *

# This module uses the pygame coordinate system.

class Line(object):

    # Factory Methods {{{1
    @staticmethod
    def from_points(head, tail, normal=Vector.null()):
        return Line(head, tail, normal)

    @staticmethod
    def from_direction(tail, direction, normal=Vector.null()):
        return Line(tail, tail + direction, normal)
    # }}}1

    # Operators {{{1
    def __init__(self, head, tail, facing=None):
        self.__head = head
        self.__tail = tail
        self.__facing = facing

        try:
            self.__normal = (head - tail).get_orthonormal()
            self.__degenerate = False
        except NullVectorError:
            self.__normal = None
            self.__degenerate = True

    def __eq__(self, other):
        if self.facing != other.facing:
            return False

        first, second = self.points
        if (first, second) == other.points: return True
        if (second, first) == other.points: return True
        return False

    def __repr__(self):
        line = "Line: %s to %s" % self.points
        facing = ", facing %s" % self.__facing

        return line + facing if self.__facing else line

    # Attributes {{{1
    @property
    def head(self):
        return self.__head

    @property
    def tail(self):
        return self.__tail

    @property
    def degenerate(self):
        return self.__degenerate

    @property
    def facing(self):
        assert self.__facing
        return self.__facing

    @property
    def normal(self):
        assert self.__normal
        return self.__normal

    @property
    def center(self):
        return (self.head + self.tail) / 2.0

    @property
    def points(self):
        return (self.head, self.tail)

    @property
    def direction(self):
        return self.head - self.tail

    def get_head(self): return self.head
    def get_tail(self): return self.tail
    def get_degenerate(self): return self.degenerate

    def get_facing(self): return self.facing
    def get_normal(self): return self.normal
    
    def get_center(self): return self.center
    def get_points(self): return self.points
    def get_direction(self): return self.direction
    # }}}1

class Circle(object):

    # Factory Methods {{{1
    def shrink(self, padding):
        return self.grow(-padding)

    def grow(self, padding):
        return Circle(self.center, self.radius + padding)

    def move(self, displacement):
        return Circle(self.center + displacement, self.radius)
    # }}}1

    # Operators {{{1
    def __init__(self, center, radius):
        self.__center = center
        self.__radius = radius

        left = center.x - radius; right = center.x + radius
        top = center.y - radius; bottom = center.y + radius

        self.__box = Rectangle(left, top, right, bottom)

    def __eq__(self, other):
        return (self.center == other.center and
                self.radius == other.radius)

    def __repr__(self):
        return "Circle: %s, r=%d" % (self.center, self.radius)

    # Attributes {{{1
    @property
    def center(self):
        return self.__center

    @property
    def radius(self):
        return self.__radius

    @property
    def box(self):
        return self.__box

    def get_center(self):
        return self.center

    def get_radius(self):
        return self.radius

    def get_box(self):
        return self.box
    # }}}1

class Shape(object):

    # Attributes {{{1
    @property
    def edges(self): raise NotImplementedError
    @property
    def vertices(self): raise NotImplementedError

    @property
    def center(self): raise NotImplementedError
    @property
    def box(self): raise NotImplementedError

    def get_edges(self): return self.edges
    def get_vertices(self): return self.vertices

    def get_center(self): return self.center
    def get_box(self): return self.box

    # Setup Methods {{{1
    @staticmethod
    def check_vertices(vertices):
        current = 0
        previous = 0

        # Make sure that these vertices don't describe a concave shape.
        for A, B, C in Polygon.yield_vertices(vertices, 3):
            first = A - B
            second = C - B

            # If the shape in concave, then the perp product of each pair of
            # edges should point in the same direction.
            current = Vector.perp(first, second)
            if current * previous < 0:
                assert False

            previous = current

        return vertices

    @staticmethod
    def find_center(vertices):
        return sum(vertices, Vector.null()) / len(vertices)

    @staticmethod
    def find_edges(vertices, center):
        edges = []
        for head, tail in Polygon.yield_vertices(vertices, 2):

            direction = (head - tail).get_orthogonal()
            normal = direction.get_normal()
            reference = center - (head + tail) / 2.0

            if Vector.dot(normal, reference) > 0:
                normal = -normal

            edge = Line(head, tail, normal)
            edges.append(edge)

        return edges

    @staticmethod
    def find_box(vertices, center):
        top, left = center.get_tuple()
        bottom, right = center.get_tuple()

        for vertex in vertices:
            top = min(top, vertex.y)
            left = min(left, vertex.x)

            bottom = max(bottom, vertex.y)
            right = max(right, vertex.y)

        return Rectangle(left, top, right, bottom)

    @staticmethod
    def yield_vertices(vertices, count):
        size = len(vertices)

        for index in range(size):
            start, end = index, index + count

            if end > size:
                end = end - size
                yield vertices[start:] + vertices[:end]
            else:
                yield vertices[start : end]
    # }}}1

class Polygon(Shape):

    # Factory Methods {{{1
    @staticmethod
    def from_vertices(vertices):
        return Polygon(vertices)

    @staticmethod
    def from_regular(center, radius, sides, angle=0):
        vertices = []

        for index in range(sides):
            normal = Vector.from_radians(2 * pi * index / sides + angle)
            vertex = center + radius * normal
            vertices.append(vertex)

        return Polygon(vertices)
    # }}}1

    # Operators {{{1
    def __init__(self, vertices):
        self.__vertices = Polygon.check_vertices(vertices)
        self.__center = Polygon.find_center(vertices)
        self.__edges = Polygon.find_edges(vertices, self.__center)
        self.__box = Polygon.find_box(vertices, self.__center)

    # Attributes {{{1
    @property
    def edges(self):
        return self.__edges

    @property
    def vertices(self):
        return self.__vertices

    @property
    def box(self):
        return self.__box

    @property
    def center(self):
        return self.__center
    # }}}1

class Hexagon(Shape):
    pass

class Rectangle(Shape):

    # Factory Methods {{{1
    @staticmethod
    def from_dimensions(left, top, right, bottom):
        return Rectangle(left, top, right, bottom)

    @staticmethod
    def from_corners(first, second):
        return Rectangle(first.x, first.y, second.x, second.y)

    @staticmethod
    def from_center(center, width, height):
        half_width = width / 2.0
        half_height = height / 2.0

        left = center.x - half_width; right = center.x + half_width
        top = center.y - half_height; bottom = center.y + half_height

        return Rectangle(left, top, right, bottom)

    @staticmethod
    def from_size(width, height):
        return Rectangle(0, 0, width, height)

    @staticmethod
    def from_top_left(corner, width, height):
        left = corner.x; right = corner.x + width
        top = corner.y; bottom = corner.y + height

        return Rectangle(left, top, right, bottom)

    @staticmethod
    def from_point(point):
        return Rectangle.from_corners(point, point)

    @staticmethod
    def from_circle(circle):
        return circle.box

    @staticmethod
    def from_shape(shape):
        return shape.box

    def shrink(self, padding):
        return self.grow(-padding)

    def grow(self, padding):
        left = self.left - padding; right = self.right + padding
        top = self.top - padding; bottom = self.bottom + padding

        if left > right:
            left = right = (left + right) / 2.0
        if top > bottom:
            top = bottom = (top + bottom) / 2.0

        return Rectangle(left, top, right, bottom)

    def move(self, displacement):
        dx, dy = displacement.get_tuple()

        left = self.left + dx; right = self.right + dx
        top = self.top + dy; bottom = self.bottom + dy

        return Rectangle(left, top, right, bottom)
    # }}}1

    # Operators {{{1
    def __init__(self, left, top, right, bottom):
        self.__left = min(left, right)
        self.__top = min(top, bottom)

        self.__right = max(right, left)
        self.__bottom = max(bottom, top)

    def __eq__(self, other):
        return (type(self) == type(other) and
                self.top == other.top and
                self.bottom == other.bottom and
                self.left == other.left and
                self.right == other.right)

    def __repr__(self):
        return "<T:%d L:%d, W:%d H:%d>" % self.dimensions

    # Attributes {{{1
    @property
    def top(self):
        return self.__top
    @property
    def bottom(self):
        return self.__bottom
    @property
    def left(self):
        return self.__left
    @property
    def right(self):
        return self.__right

    @property
    def dimensions(self):
        return (self.top, self.left, self.width, self.height)

    @property
    def width(self):
        return abs(self.left - self.right)
    @property
    def height(self):
        return abs(self.top - self.bottom)
    @property
    def size(self):
        return (self.width, self.height)

    @property
    def top_left(self):
        return Vector(self.left, self.top)
    @property
    def top_right(self):
        return Vector(self.right, self.top)
    @property
    def bottom_left(self):
        return Vector(self.left, self.bottom)
    @property
    def bottom_right(self):
        return Vector(self.right, self.bottom)

    @property
    def corners(self):
        return (self.top_left, self.bottom_right)

    @property
    def top_edge(self):
        return Line(self.top_left, self.top_right, Vector(0, -1))
    @property
    def bottom_edge(self):
        return Line(self.bottom_left, self.bottom_right, Vector(0, 1))
    @property
    def left_edge(self):
        return Line(self.top_left, self.bottom_left, Vector(-1, 0))
    @property
    def right_edge(self):
        return Line(self.top_right, self.bottom_right, Vector(1, 0))

    @property
    def edges(self):
        return (self.top_edge, self.bottom_edge,
                self.left_edge, self.right_edge)

    @property
    def vertices(self):
        return (self.top_left, self.top_right,
                self.bottom_right, self.bottom_left)

    @property
    def center(self):
        x = (self.left + self.right) / 2.0
        y = (self.top + self.bottom) / 2.0
        return Vector(x, y)

    @property
    def box(self):
        return self

    def get_top(self): return self.top
    def get_bottom(self): return self.bottom
    def get_left(self): return self.left
    def get_right(self): return self.right

    def get_dimensions(self): return self.dimensions

    def get_width(self): return self.width
    def get_height(self): return self.height
    def get_size(self): return self.size

    def get_top_left(self): return self.top_left
    def get_top_right(self): return self.top_right
    def get_bottom_left(self): return self.bottom_left
    def get_bottom_right(self): return self.bottom_right

    def get_corners(self): return self.corners

    def get_top_edge(self): return self.top_edge
    def get_bottom_edge(self): return self.bottom_edge
    def get_left_edge(self): return self.left_edge
    def get_right_edge(self): return self.right_edge
    # }}}1

if __name__ == "__main__":
    from pprint import *

    # Line Tests {{{1
    def line_tests():
        head = Vector(10, 0); tail = Vector(0, 0)
        normal = Vector(0, 1); opposite = Vector(0, -1)

        direction = Vector(10, 0)
        different = Vector(5, 5)

        line = Line.from_points(head, tail, normal)

        assert line.get_head() == head
        assert line.get_tail() == tail
        assert line.get_normal() == normal

        assert line.get_center() == Vector(5, 0)
        assert line.get_degenerate() == False

        assert line.get_points() == (head, tail)
        assert line.get_direction() == Vector(10, 0)

        same_line = Line.from_direction(tail, direction, normal)
        opposite_line = Line.from_points(head, tail, opposite)

        assert line == same_line
        assert not line == opposite_line

    # Circle Tests {{{1
    def circle_tests():
        center = Vector(15, 15); radius = 5
        displacement = Vector(5, 5)

        circle = Circle(center, radius)
        box = Rectangle.from_center(center, 10, 10)

        assert circle == circle
        assert circle.get_box() == box

        assert circle.get_center() == center
        assert circle.get_radius() == radius

        grown_circle = Circle(center, radius - 1).grow(1)
        shrunk_circle = Circle(center, radius + 1).shrink(1)
        moved_circle = Circle(
                center - displacement, radius).move(displacement) 

        assert grown_circle == circle
        assert shrunk_circle == circle
        assert moved_circle == circle

    # Shape Tests {{{1
    def polygon_tests():
        top_left = Vector(10, 10); top_right = Vector(20, 10)
        bottom_left = Vector(10, 20); bottom_right = Vector(20, 20)

        vertices = [top_left, top_right, bottom_right, bottom_left]
        bad_vertices = [top_left, top_right, bottom_left, bottom_right]

        try: Polygon(bad_vertices)
        except AssertionError:
            pass            # Concave polygon rejected.
        else:
            assert False    # Concave polygon created.

        polygon = Polygon(vertices)

        top = Vector(0, -1); bottom = Vector(0, 1)
        left = Vector(-1, 0); right = Vector(1, 0)

        center = Vector(15, 15)
        box = Rectangle.from_corners(top_left, bottom_right)

        edges = [
                Line(top_left, top_right, top),
                Line(top_right, bottom_right, right),
                Line(bottom_right, bottom_left, bottom),
                Line(bottom_left, top_left, left) ]

        assert polygon.get_box() == box
        assert polygon.get_center() == center

        for edge in edges:
            assert edge in polygon.edges
        for vertex in vertices:
            assert vertex in polygon.vertices

    # Rectangle Tests {{{1
    def rectangle_tests():

        top = 0; bottom = 4; left = 0; right = 2
        width = right - left; height = bottom - top
        center = Vector(left + right, top + bottom) / 2

        edges = [
                Line(Vector(left, top), Vector(right, top), Vector(0, -1)),
                Line(Vector(right, top), Vector(right, bottom), Vector(1, 0)),
                Line(Vector(right, bottom), Vector(left, bottom), Vector(0, 1)),
                Line(Vector(left, bottom), Vector(left, top), Vector(-1, 0)) ]

        vertices = [
                Vector(left, top), Vector(right, top),
                Vector(left, bottom), Vector(right, bottom) ]

        golden = Rectangle.from_dimensions(left, top, right, bottom)

        assert golden.size == (width, height)
        assert golden.dimensions == (top, left, width, height)

        assert golden.center == center
        assert golden.box == golden

        for edge in edges:
            assert edge in golden.edges
        for vertex in vertices:
            assert vertex in golden.vertices

        assert golden == Rectangle.from_size(width, height)
        assert golden == Rectangle.from_center(center, width, height)

        assert golden == Rectangle.from_corners(
                Vector(left, top), Vector(right, bottom))
        assert golden == Rectangle.from_top_left(
                Vector(left, top), width, height)

        assert golden == Rectangle(
                left + 1, top + 1, right - 1, bottom - 1).grow(1)
        assert golden == Rectangle(
                left - 1, top - 1, right + 1, bottom + 1).shrink(1)
        assert golden == Rectangle(
                left - 1, top - 1, right - 1, bottom - 1).move(Vector(1, 1))

    # }}}1

    print "Testing shapes.py..."

    line_tests()
    circle_tests()
    polygon_tests()
    rectangle_tests()

    print "All tests passed."

