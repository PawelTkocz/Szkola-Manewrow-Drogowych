from car.model import SteeringSystemSpecification
from geometry.direction import Direction
from schemas import HorizontalDirection


class SteeringSystem:
    def __init__(
        self, specification: SteeringSystemSpecification, current_wheels_angle: float
    ) -> None:
        self._wheels_turn_speed = specification["wheels_turn_speed"]
        self._wheels_max_angle = specification["wheels_max_angle"]
        self._wheels_min_angle = -1 * specification["wheels_max_angle"]
        self._current_wheels_angle = current_wheels_angle

    @property
    def wheels_angle(self) -> float:
        return self._current_wheels_angle

    def get_wheels_direction(self, car_direction: Direction) -> Direction:
        return car_direction.copy().turn(self._current_wheels_angle)

    def turn(self, direction: HorizontalDirection) -> None:
        turn_angle = (
            self._wheels_turn_speed
            if direction == HorizontalDirection.LEFT
            else -1 * self._wheels_turn_speed
        )
        self._current_wheels_angle = max(
            self._wheels_min_angle,
            min(self._current_wheels_angle + turn_angle, self._wheels_max_angle),
        )
