import math
from geometry.vector import Point, Vector


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
