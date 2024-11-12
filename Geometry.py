from enum import Enum
import math
from typing import List


class Directions(Enum):
    RIGHT = 1
    LEFT = 2
    FRONT = 3
    BACK = 4


class Point:
    """
    Class representing a point in Cartesian coordinate system
    """

    def __init__(self, x: float, y: float):
        """
        Initialize point with coordinates (x, y)

        :param x: x coordinate
        :param y: y coordinate
        :return: Point with coordinates (x, y)
        """
        self.x = x
        self.y = y

    def compare(self, point: "Point") -> bool:
        """
        Check if two points are equal

        :param point: Point to compare with
        :return: True iff coordinates of points are equal
        """
        return self.x == point.x and self.y == point.y

    def add_vector(self, vector: "Vector") -> "Point":
        """
        Add vector to point

        :param vector: Vector to add
        :return: Point translated by vector
        """
        self.x += vector.x
        self.y += vector.y
        return self

    def copy(self) -> "Point":
        """
        Get copy of a point
        """
        return Point(self.x, self.y)

    def rotate_over_point(self, rotate_point: "Point", angle: float) -> "Point":
        """
        Rotate this point over some other point

        :param rotate_point: Point to rotate over
        :param angle: angle (in radians) of the rotation
        :param dir: direction of the rotation
        :return: Point after the rotation
        """
        # if angle is always positive then there is a need to do
        # angle = math.pi * 2 - angle if dir == Directions.RIGHT else angle
        sin = math.sin(angle)
        cos = math.cos(angle)

        v = Vector(end=self, start=rotate_point)
        v_rotated = Vector(
            Point(v.x * cos - v.y * sin, v.x * sin + v.y * cos)
        ).scale_to_len(v.len())
        rotated_point = rotate_point.copy().add_vector(v_rotated)
        self.x = rotated_point.x
        self.y = rotated_point.y
        return self


class Vector(Point):
    """
    Class representing a position vector in Cartesian coordinate system

    Position vector is represented by single Point P, and is
    identified with the vector from (0, 0) to P
    """

    def __init__(self, end: Point, start: Point = Point(0, 0)):
        """
        Initialize position vector of vector [start, end]

        :param end: end point of the vector
        :param start: start point of the vector
        :return: position vector of vector [start, end]
        """
        super().__init__(end.x - start.x, end.y - start.y)

    def len(self) -> float:
        """
        Get the length of the vector
        """
        return math.sqrt(self.x**2 + self.y**2)

    def scale(self, k: float) -> "Vector":
        """
        Multiply the vector by scalar

        :param k: scalar value
        :return: Vector scaled by k
        """
        self.x *= k
        self.y *= k
        return self

    def scale_to_len(self, len: float) -> "Vector":
        """
        Scale the vector to specified length

        :param len: desired length of result vector
        :return: Vector scaled to specified length
        """
        if self.len() == 0:
            return self
        else:
            return self.scale(len / self.len())

    def get_orthogonal_vector(
        self, dir: Directions, len: float | None = None
    ) -> "Vector":
        """
        Get orthogonal vector

        :param dir: direction of the 'turn' for orthogonal vector
        :param len: length of result vector (length unchanged if len is None)
        :return: orthogonal vector with desired length
        """
        if dir not in [Directions.LEFT, Directions.RIGHT]:
            return self.copy()
        v = (
            Vector(Point(self.y, -1 * self.x))
            if dir == Directions.RIGHT
            else Vector(Point(-1 * self.y, self.x))
        )
        return v.scale_to_len(len) if len is not None else v

    def get_negative_of_a_vector(self):
        return self.copy().scale(-1)

    def normalize(self) -> "Vector":
        """
        Scale the vector to the length of 1
        """
        return self.scale_to_len(1)

    def copy(self) -> "Vector":
        """
        Get copy of vector
        """
        return Vector(self)


class Direction(Vector):
    """
    Class representing direction as a normalized position vector
    """

    def __init__(self, end: Point, start: Point = Point(0, 0)):
        super().__init__(end, start)
        super().normalize()

    def turn(self, angle: float) -> "Direction":
        """
        Change the direction

        :param angle: angle (in radians) of the turn
        :return: Direction after the turn
        """
        super().rotate_over_point(Point(0, 0), angle)
        super().normalize()
        return self

    def copy(self) -> "Direction":
        """
        Get copy of direction
        """
        return Direction(self)

    @property
    def sinus(self) -> float:
        return min(self.y, 1) if self.y > 0 else max(self.y, -1)

    @property
    def cosinus(self) -> float:
        return min(self.x, 1) if self.x > 0 else max(self.x, -1)

    @property
    def angle(self) -> float:
        """
        Returns the angle represented by direction vector

        The angle is in range [0, pi] when direction.y >= 0
        and in range [-pi, 0] when direction.y < 0
        """
        cos = math.acos(self.cosinus)
        return cos if self.y > 0 else -1 * cos


class Rectangle:
    """
    Class representing 'directed' rectangle in Cartesian coordinate system

    'Directed' rectangle has its front, left and right side, and rear
    """

    def __init__(
        self, front_middle: Point, width: float, length: float, direction: Direction
    ):
        """
        Initialize directed rectangle

        :param front_middle: position of front middle point of the rectangle
        :param width: width of the rectangle (of front and rear sides)
        :param length: length of the rectangle (of left and right sides)
        :param direction: direction the rectangle is heading
        :return: directed rectangle with specified width, length and position
        """
        self.width = width
        self.length = length
        self._direction = direction.copy()
        self._front_middle = front_middle.copy()
        width_vec = direction.get_orthogonal_vector(Directions.RIGHT, width)
        length_vec = width_vec.get_orthogonal_vector(Directions.RIGHT, length)
        self._front_left = front_middle.copy().add_vector(
            width_vec.copy().scale(0.5).get_negative_of_a_vector()
        )
        self._front_right = self._front_left.copy().add_vector(width_vec)
        self._rear_left = self._front_left.copy().add_vector(length_vec)
        self._rear_right = self._rear_left.copy().add_vector(width_vec)

    @property
    def direction(self) -> Direction:
        """
        Get the current direction of the rectangle
        """
        return self._direction.copy()
        # remember to calculate it everytime position changes

    @property
    def front_middle(self) -> Point:
        return self._front_middle.copy()

    @property
    def front_left(self) -> Point:
        return self._front_left.copy()

    @property
    def front_right(self) -> Point:
        return self._front_right.copy()

    @property
    def rear_left(self) -> Point:
        return self._rear_left.copy()

    @property
    def rear_right(self) -> Point:
        return self._rear_right.copy()

    @property
    def corners_list(self) -> List[Point]:
        """
        Get the list of corners coordinates
        """
        return [
            self.rear_left,
            self.rear_right,
            self.front_right,
            self.front_left,
        ]

    @property
    def center(self) -> Point:
        """
        Get the center of rectangle
        """
        vector = Vector(self.rear_right, self.front_left).scale(0.5)
        return self.front_left.add_vector(vector)

    def move_left_side(self, front_vector: Vector):
        self._front_left.add_vector(front_vector)
        length_vector = Vector(self.front_left, self.rear_left).scale_to_len(
            self.length
        )
        width_vector = length_vector.get_orthogonal_vector(Directions.RIGHT, self.width)
        self._front_right = self.front_left.add_vector(width_vector)
        self._rear_right = self.front_right.add_vector(
            length_vector.get_negative_of_a_vector()
        )
        self._rear_left = self.front_left.add_vector(
            length_vector.get_negative_of_a_vector()
        )
        self._direction = Direction(self.front_left, self.rear_left)
        self._front_middle = self.front_left.add_vector(width_vector.scale(0.5))

    def move_right_side(self, front_vector: Vector):
        self._front_right.add_vector(front_vector)
        length_vector = Vector(self.front_right, self.rear_right).scale_to_len(
            self.length
        )
        width_vector = length_vector.get_orthogonal_vector(Directions.LEFT, self.width)
        self._front_left = self.front_right.add_vector(width_vector)
        self._rear_left = self.front_left.add_vector(
            length_vector.get_negative_of_a_vector()
        )
        self._rear_right = self.front_right.add_vector(
            length_vector.get_negative_of_a_vector()
        )
        self._direction = Direction(self.front_left, self.rear_left)
        self._front_middle = self.front_right.add_vector(width_vector.scale(0.5))

    def collides(self, obj: "Rectangle"):
        pass


# maybe create class Angle for wheels angle and class Direction whill extend this class
