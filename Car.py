import math
from Geometry import Direction, Point, Rectangle


class Car:
    """
    Class representing a car in Cartesian coordinate system
    """

    def __init__(
        self,
        width: float,
        length: float,
        front_left_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        max_wheels_turn: float = math.pi / 3,
        color: str = "red",
        velocity: float = 0,
        max_velocity: float = 10,
        max_acceleration: float = 1,
    ):
        """
        Initialize car
        """
        self.width = width
        self.length = length
        self.body = Rectangle(front_left_position, width, length, direction)
        # self.wheels = Wheels(max_wheels_turn)
        self.velocity = velocity
        # self.car_drafter = CarDrafter(width, length, color)

    @property
    def direction(self):
        return self.body.direction

    @property
    def front_left(self):
        return self.rect.front_left

    @property
    def front_right(self):
        return self.rect.front_right

    @property
    def rear_left(self):
        return self.rect.rear_left

    @property
    def rear_right(self):
        return self.rect.rear_right
