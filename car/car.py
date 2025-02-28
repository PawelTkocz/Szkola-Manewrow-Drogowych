from enum import Enum
from geometry import Direction, Directions, Point, Rectangle, Vector
from car.model import CarModel
from car.wheels import Wheels
from drafter.car import CarDrafter


class SpeedModifications(Enum):
    SPEED_UP = 1
    NO_CHANGE = 2
    BRAKE = 3


class CarBody(Rectangle):
    def __init__(
        self, front_middle: Point, width: float, length: float, direction: Direction
    ):
        super().__init__(front_middle, width, length, direction)

    def move(self, direction: Directions, front_vector: Vector):
        if direction == Directions.RIGHT:
            self.move_left_side(front_vector)
        else:
            self.move_right_side(front_vector)
        # czemu zmiana z left na right i odwrotnie rozwiazuje problem z tym, ze jadac prosto
        # zblizalismy sie wolniej do celu niz skrecajac

    # think about unifying this to just move - vector from front middle
    def move_left_side(self, front_vector: Vector):
        new_front_left = self.front_left.add_vector(front_vector)
        length_vector = Vector(new_front_left, self.rear_left).scale_to_len(self.length)
        new_rear_left = new_front_left.copy().add_vector(
            length_vector.get_negative_of_a_vector()
        )
        new_direction = Direction(new_front_left, new_rear_left)
        new_front_middle = new_front_left.copy().add_vector(
            length_vector.get_orthogonal_vector(Directions.RIGHT, self.width / 2)
        )
        self.update_position(new_front_middle, new_direction)

    def move_right_side(self, front_vector: Vector):
        new_front_right = self.front_right.add_vector(front_vector)
        length_vector = Vector(new_front_right, self.rear_right).scale_to_len(
            self.length
        )
        new_rear_right = new_front_right.copy().add_vector(
            length_vector.get_negative_of_a_vector()
        )
        new_direction = Direction(new_front_right, new_rear_right)
        new_front_middle = new_front_right.copy().add_vector(
            length_vector.get_orthogonal_vector(Directions.LEFT, self.width / 2)
        )
        self.update_position(new_front_middle, new_direction)


class Car(CarBody):
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
        super().__init__(front_middle_position, model.width, model.length, direction)
        self.model = model
        self.color = color
        self.velocity = velocity
        self.wheels = Wheels(model.max_wheels_turn)
        self._car_drafter = CarDrafter(model, color)

    @property
    def wheels_angle(self) -> float:
        return self.wheels.angle

    @property
    def turn_direction(self) -> Directions:
        return self.wheels.current_direction

    @property
    def max_acceleration(self) -> float:
        return self.model.max_acceleration

    @property
    def max_velocity(self) -> float:
        return self.model.max_velocity

    @property
    def max_brake(self) -> float:
        return self.model.max_brake

    @property
    def wheels_turn_speed(self) -> float:
        return self.model.wheels_turn_speed

    @property
    def wheels_direction(self) -> Direction:
        return self.wheels.direction

    def turn(self, direction: Directions):
        self.wheels.turn(self.wheels_turn_speed, direction)

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
        super().move(self.turn_direction, front_movement_vector)
        self.slow_down(self.model.resistance)

    def draw(self, screen):
        self._car_drafter.draw(self, self.wheels_angle, screen)

    def collides(self, obj: Rectangle):
        if obj is not None:
            return self.collides(obj)
        return False

    def get_state(self) -> "LiveCarData":
        return LiveCarData(self)


# call it CarLiveData, include model in properties and refactor all places
class LiveCarData:
    """
    Read-only proxy for Car providing data possibly useful for other road users.
    """

    def __init__(self, car: Car):
        self._car = car

    @property
    def velocity(self) -> float:
        return self._car.velocity

    @property
    def front_middle(self) -> Point:
        return self._car.front_middle

    @property
    def direction(self) -> Direction:
        return self._car.direction

    @property
    def front_left(self) -> Point:
        return self._car.front_left

    @property
    def front_right(self) -> Point:
        return self._car.front_right

    @property
    def rear_left(self) -> Point:
        return self._car.rear_left

    @property
    def rear_right(self) -> Point:
        return self._car.rear_right

    @property
    def wheels_angle(self) -> float:
        return self._car.wheels_angle

    @property
    def length(self) -> float:
        return self._car.length

    @property
    def width(self) -> float:
        return self._car.width

    @property
    def max_acceleration(self) -> float:
        return self._car.max_acceleration

    @property
    def max_velocity(self) -> float:
        return self._car.max_velocity

    @property
    def max_brake(self) -> float:
        return self._car.max_brake

    @property
    def model(self) -> CarModel:
        return self._car.model

    @property
    def color(self) -> str:
        return self._car.color
