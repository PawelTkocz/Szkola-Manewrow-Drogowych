from __future__ import annotations
from car.instruction_controlled_car import (
    CarMovementInstructions,
)
from car.model import CarModelSpecification
from geometry.direction import Direction
from geometry.shapes.rectangle import Rectangle
from geometry.vector import Point
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
        wheels_angle: float,
        velocity: float,
        model_specification: CarModelSpecification,
        *,
        registry_number: str = "",
        high_priority: bool = False,
    ) -> None:
        """
        Initialize car simulation.
        """
        self._car = smart_city_car.SmartCityCar(
            registry_number,
            model_specification,
            front_middle,
            direction,
            velocity,
            wheels_angle,
            high_priority=high_priority,
        )

    @classmethod
    def from_live_car_data(
        cls: type["CarSimulation"], live_car_data: LiveCarData
    ) -> CarSimulation:
        return cls(
            live_car_data["live_state"]["front_middle"],
            live_car_data["live_state"]["direction"],
            live_car_data["live_state"]["wheels_angle"],
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
        return self._car.max_velocity

    @property
    def body(self) -> Rectangle:
        return self._car.chassis

    @property
    def direction(self) -> Direction:
        return self._car.direction

    @property
    def acceleration(self) -> float:
        return self._car.acceleration

    @property
    def wheels_angle(self) -> float:
        return self._car.wheels_angle

    @property
    def body_safe_zone(self) -> Rectangle:
        return Rectangle(
            self._car.front_middle.add_vector(
                self._car.direction.scale_to_len(1.5 * self._car.length)
            ),
            self._car.width * 1.5,
            self._car.length * 4,
            self._car.direction,
        )

    def set_velocity(self, velocity: float) -> None:
        self._car.velocity = velocity
