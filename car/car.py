from pygame import Surface
from car.turn_signals import TurnSignals
from geometry import Direction, Directions, Point, Rectangle, Vector
from car.model import CarModel
from car.wheels import Wheels
from drafter.car import CarDrafter
from schemas import HorizontalDirection


class CarBody(Rectangle):
    def __init__(
        self, front_middle: Point, width: float, length: float, direction: Direction
    ):
        super().__init__(front_middle, width, length, direction)

    def _force_move(self, front_vector: Vector) -> None:
        new_front_middle = self.front_middle.add_vector(front_vector)
        length_vector = Vector(new_front_middle, self.rear_middle).scale_to_len(
            self.length
        )
        new_rear_middle = new_front_middle.copy().add_vector(
            length_vector.get_negative_of_a_vector()
        )
        new_direction = Direction(new_front_middle, new_rear_middle)
        self.update_position(new_front_middle, new_direction)


class Car(CarBody):
    """
    Class representing a car in Cartesian coordinate system.
    """

    def __init__(
        self,
        registry_number: str,
        model: CarModel,
        color: str,
        front_middle_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
        wheels_direction: Direction = Direction(Point(1, 0)),
        turn_signal: HorizontalDirection | None = HorizontalDirection.LEFT,
    ):
        """
        Initialize car
        """
        super().__init__(front_middle_position, model.width, model.length, direction)
        self.registry_number = registry_number
        self.model = model
        self.color = color
        self.velocity = velocity
        self.wheels = Wheels(model.max_wheels_turn, wheels_direction)
        self.turn_signals = TurnSignals(model.turn_signals_tick_interval, turn_signal)
        self._car_drafter = CarDrafter()

    @property
    def wheels_angle(self) -> float:
        return self.wheels.angle

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

    def turn_left(self) -> None:
        self.wheels.turn(self.wheels_turn_speed, HorizontalDirection.LEFT)

    def turn_right(self) -> None:
        self.wheels.turn(self.wheels_turn_speed, HorizontalDirection.RIGHT)

    def accelerate(self, direction: Directions) -> None:
        if direction == Directions.FRONT:
            self.velocity = min(
                self.velocity + self.max_acceleration, self.max_velocity
            )
        elif direction == Directions.BACK:
            self.velocity = max(
                self.velocity - self.max_acceleration, -1 * self.max_velocity
            )

    def _slow_down(self, value: float) -> None:
        self.velocity = (
            max(self.velocity - value, 0)
            if self.velocity > 0
            else min(self.velocity + value, 0)
        )

    def brake(self) -> None:
        self._slow_down(self.max_brake)

    def acitvate_turn_signal(self, side: HorizontalDirection) -> None:
        self.turn_signals.activate(side)

    def deactivate_turn_signal(self) -> None:
        self.turn_signals.deactivate()

    def move(self) -> None:
        if self.velocity == 0:
            return

        front_movement_vector = self.direction.turn(self.wheels_angle).scale_to_len(
            self.velocity
        )
        self._force_move(front_movement_vector)
        self._slow_down(self.model.resistance)

    def draw(
        self, screen: Surface, *, scale: float = 1, screen_y_offset: int = 0
    ) -> None:
        self._car_drafter.draw(
            self.model,
            self.color,
            self,
            self.wheels_angle,
            self.turn_signals.are_turn_signals_lights_on(),
            screen,
            scale=scale,
            screen_y_offset=screen_y_offset,
        )

    def tick(self) -> None:
        self.move()
        self.turn_signals.tick()
