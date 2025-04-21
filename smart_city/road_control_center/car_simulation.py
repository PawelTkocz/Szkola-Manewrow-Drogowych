from car.instruction_controlled_car import (
    CarMovementInstructions,
)
from car.model import CarModel
from geometry.direction import Direction
from geometry.vector import Point
from geometry.rectangle import Rectangle
from smart_city.schemas import LiveCarData
import smart_city.smart_city_car as smart_city_car


class CarSimulation:
    """
    Class simulating smart city car.
    """

    def __init__(
        self,
        front_middle: Point,
        direction: Direction,
        wheels_direction: Direction,
        velocity: float,
        model: CarModel,
        *,
        registry_number: str = "",
        high_priority: bool = False,
    ) -> None:
        """
        Initialize car simulation.
        """
        self._car = smart_city_car.SmartCityCar(
            registry_number,
            model,
            front_middle,
            direction,
            velocity,
            wheels_direction,
            high_priority=high_priority,
        )

    @classmethod
    def from_live_car_data(
        cls: type["CarSimulation"], live_car_data: LiveCarData
    ) -> "CarSimulation":
        return cls(
            live_car_data["live_state"]["front_middle"],
            live_car_data["live_state"]["direction"],
            live_car_data["live_state"]["wheels_direction"],
            live_car_data["live_state"]["velocity"],
            live_car_data["specification"]["model"],
            registry_number=live_car_data["specification"]["registry_number"],
            high_priority=live_car_data["live_state"]["high_priority"],
        )

    def get_live_data(self) -> LiveCarData:
        return self._car.get_live_data()

    def move(
        self, movement_instructions: CarMovementInstructions | None = None
    ) -> None:
        if movement_instructions:
            self._car._apply_movement_instructions(movement_instructions)
        self._car.move()

    def collides(self, obj: Rectangle) -> bool:
        return self._car.collides(obj)

    def is_point_inside(self, point: Point) -> bool:
        return self._car.is_point_inside(point)

    @property
    def velocity(self) -> float:
        return self._car.velocity

    @property
    def front_middle(self) -> Point:
        return self._car.front_middle

    @property
    def max_velocity(self) -> float:
        return self._car.model.max_velocity

    @property
    def body(self) -> Rectangle:
        return self._car
