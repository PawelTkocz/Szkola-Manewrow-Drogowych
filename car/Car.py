from enum import Enum
from geometry import Direction, Directions, Point, Rectangle
from car.model import CarModel
from car.wheels import Wheels
from drafter.car import CarDrafter


class SpeedModifications(Enum):
    SPEED_UP = 1
    NO_CHANGE = 2
    BRAKE = 3


class Car:
    """
    Class representing a car in Cartesian coordinate system.
    """

    def __init__(
        self,
        model: CarModel,
        color: str,
        front_middle_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
    ):
        """
        Initialize car
        """
        self.model = model
        self.color = color
        self.velocity = velocity
        self.body = Rectangle(
            front_middle_position,
            model.width,
            model.length,
            direction,
        )
        self.wheels = Wheels(model.max_wheels_turn)
        self._car_drafter = CarDrafter(model, color)

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
        return self.model.length

    @property
    def width(self) -> float:
        return self.model.width

    @property
    def max_acceleration(self) -> float:
        return self.model.max_acceleration

    @property
    def max_velocity(self) -> float:
        return self.model.max_velocity

    @property
    def max_brake(self) -> float:
        return self.model.max_brake

    def turn(self, direction: Directions):
        self.wheels.turn(self.model.wheels_turn_speed, direction)

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

    def apply_speed_modification(self, modification: SpeedModifications):
        if modification == SpeedModifications.SPEED_UP:
            direction = Directions.FRONT if self.velocity >= 0 else Directions.BACK
            self.speed_up(direction)
        elif modification == SpeedModifications.NO_CHANGE:
            pass
        elif modification == SpeedModifications.BRAKE:
            self.brake()

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
        self.slow_down(self.model.resistance)

    def draw(self, screen):
        self._car_drafter.draw(self.body, self.wheels_angle, screen)

    def collides(self, obj: Rectangle):
        if obj is not None:
            return self.body.collides(obj)
        return False

    def get_state(self):
        return {
            "velocity": self.velocity,
            "body": {
                "direction": self.direction,
                "front_middle": self.front_middle,
                "front_left": self.front_left,
                "front_right": self.front_right,
                "rear_left": self.rear_left,
                "rear_right": self.rear_right,
            },
            "wheels": self.wheels.direction.copy(),
        }
