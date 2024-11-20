from enum import Enum
import math
from Geometry import Direction, Directions, Point, Rectangle, Vector
from cars.Brand import Brand
from cars.Wheels import Wheels


class CarParts(Enum):
    BUMPERS = 1  # obwod samochodu
    BODY = 2  # karoseria
    FRONT_WHEELS = 3
    FRONT_LIGHTS = 4
    SIDE_MIRRORS = 5
    FRONT_WINDOW = 6
    SIDE_WINDOW = 7
    BACK_WINDOW = 8


class Car:
    """
    Class representing a car in Cartesian coordinate system
    """

    def __init__(
        self,
        brand: Brand,
        front_middle_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
    ):
        """
        Initialize car
        """
        self.brand = brand
        self.velocity = velocity
        self.body = Rectangle(
            front_middle_position, brand.width, brand.length, direction
        )
        self.wheels = Wheels(self.brand.max_wheels_turn)

    @property
    def front_middle(self) -> Point:
        return self.body.front_middle

    @property
    def direction(self) -> Direction:
        return self.body.direction

    @property
    def front_left(self) -> Point:
        return self.body.front_left

    @property
    def front_right(self) -> Point:
        return self.body.front_right

    @property
    def rear_left(self) -> Point:
        return self.body.rear_left

    @property
    def rear_right(self) -> Point:
        return self.body.rear_right

    @property
    def wheels_angle(self) -> float:
        return self.wheels.angle

    @property
    def turn_direction(self) -> Directions:
        return self.wheels.current_direction

    @property
    def length(self) -> float:
        return self.brand.length

    @property
    def width(self) -> float:
        return self.brand.width

    @property
    def max_acceleration(self) -> float:
        return self.brand.max_acceleration

    @property
    def max_velocity(self) -> float:
        return self.brand.max_velocity

    @property
    def max_brake(self) -> float:
        return self.brand.max_brake

    def turn(self, direction: Directions):
        self.wheels.turn(self.brand.wheels_turn_speed, direction)

    def speed_up(self, direction: Directions, limit=None):
        if (self.velocity > 0 and direction == Directions.BACK) or (
            self.velocity < 0 and direction == Directions.FRONT
        ):
            return
        if limit is not None and abs(self.velocity) > limit:
            self.brake()
            return
        if direction == Directions.FRONT:
            self.velocity = min(
                self.velocity + self.max_acceleration,
                self.max_velocity,
                limit if limit is not None else self.max_velocity,
            )
        elif direction == Directions.BACK:
            self.velocity = max(
                self.velocity - self.max_acceleration,
                -1 * self.max_velocity,
                limit if limit is not None else -1 * self.max_velocity,
            )

    def slow_down(self, value):
        self.velocity = (
            max(self.velocity - value, 0)
            if self.velocity > 0
            else min(self.velocity + value, 0)
        )

    def brake(self):
        self.slow_down(self.max_brake)

    def move(self):
        if self.velocity == 0:
            return

        front_movement_vector = self.direction.turn(self.wheels_angle).scale_to_len(
            self.velocity
        )
        if self.turn_direction == Directions.RIGHT:
            self.body.move_left_side(front_movement_vector)
        else:
            self.body.move_right_side(front_movement_vector)
        # czemu zmiana z left na right i odwrotnie rozwiazuje problem z tym, ze jadac prosto
        # zblizalismy sie wolniej do celu niz skrecajac
        self.slow_down(self.brand.resistance)

    def draw(self, screen):
        self.brand.draw(self.body, self.wheels_angle, screen)

    def collides(self, obj: Rectangle):
        pass
