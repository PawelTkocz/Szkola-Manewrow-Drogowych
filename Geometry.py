from enum import Enum
import math


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

    def rotate_over_point(
        self, rotate_point: "Point", angle: float, dir: Directions
    ) -> "Point":
        """
        Rotate this point over some other point

        :param rotate_point: Point to rotate over
        :param angle: angle (in radians) of the rotation
        :param dir: direction of the rotation
        :return: Point after the rotation
        """
        if dir not in [Directions.LEFT, Directions.RIGHT]:
            return self
        # if angle is always positive then there is a need to do
        # angle = math.pi * 2 - angle if dir == Directions.RIGHT else angle
        sin = math.sin(angle)
        cos = math.cos(angle)

        v = Vector(end=self, start=rotate_point)
        v_rotated = Vector(Point(v.x * cos - v.y * sin, v.x * sin + v.y * cos))
        rotated_point = rotate_point.copy().add_vector(v_rotated)
        self.x = rotated_point.x
        self.y = rotated_point.y
        return self


class Vector:
    """
    Class representing a position vector in Cartesian coordinate system

    Position vector is represented by single Point P, and is
    identified with the vector from (0, 0) to P
    """

    def __init__(self, end: Point, start: Point = Point(0, 0)):
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
            return self
        v = (
            Vector(Point(self.y, -1 * self.x))
            if dir == Directions.RIGHT
            else Vector(Point(-1 * self.y, self.x))
        )
        return v.scale_to_len(len) if len else v

    def normalize(self) -> "Vector":
        """
        Scale the vector to the length of 1
        """
        return self.scale_to_len(1)
