from car.instruction_controlled_car import CarControlInstructions
from car.model import CarModel
from geometry import Direction, Point, Rectangle
from schemas import CardinalDirection
from smart_city.road_control_center.manoeuvres.schemas import (
    IntersectionManoeuvreDescription,
)
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
        manoeuvre_description: IntersectionManoeuvreDescription = {
            "starting_side": CardinalDirection.LEFT,
            "ending_side": CardinalDirection.RIGHT,
        },
        registry_number: str = "",
        color: str = "red",
        high_priority: bool = False,
    ) -> None:
        """
        Initialize car simulation.
        """
        self.car = smart_city_car.SmartCityCar(
            manoeuvre_description,
            registry_number,
            model,
            color,
            front_middle,
            direction,
            velocity,
            wheels_direction,
            high_priority,
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
            color=live_car_data["specification"]["color"],
            high_priority=live_car_data["live_state"]["high_priority"],
        )

    def get_live_data(self) -> LiveCarData:
        return self.car.get_live_data()

    def move(self, control_instructions: CarControlInstructions | None = None) -> None:
        self.car.move(
            control_instructions["movement_instructions"]
            if control_instructions
            else None
        )

    def collides(self, obj: Rectangle) -> bool:
        return self.car.collides(obj)

    @property
    def velocity(self) -> float:
        return self.car.velocity

    @property
    def front_middle(self) -> Point:
        return self.car.front_middle
