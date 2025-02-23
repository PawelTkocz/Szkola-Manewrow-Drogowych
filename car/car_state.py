from car.car import Car
from car.model import CarModel
from geometry import Direction, Point, Rectangle


# call it CarData, include model in properties and refactor all places
class CarState:
    """
    Read-only proxy for Car representing car state.
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

    def collides(self, obj: Rectangle) -> bool:
        return self._car.collides(obj)
