from car.instruction_controlled_car import (
    CarControlInstructions,
    SpeedInstruction,
    TurnInstruction,
    TurnSignalsInstruction,
)
from car.model import CarModel
from geometry import Direction, Point, Rectangle
from smart_city.road_control_center.manoeuvres.track import Track
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
        self.car = smart_city_car.SmartCityCar(
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
        return self.car.get_live_data()

    def move(self, control_instructions: CarControlInstructions | None = None) -> None:
        if control_instructions:
            self.car._apply_movement_instructions(
                control_instructions["movement_instructions"]
            )
        self.car.move()

    def collides(self, obj: Rectangle) -> bool:
        return self.car.collides(obj)

    @property
    def velocity(self) -> float:
        return self.car.velocity

    @property
    def front_middle(self) -> Point:
        return self.car.front_middle

    def get_turn_instruction(
        self,
        track: Track,
        speed_instruction: SpeedInstruction,
    ) -> TurnInstruction:
        def _distance_to_track_after_instruction(
            turn_instruction: TurnInstruction,
        ) -> float:
            car_simulation = CarSimulation.from_live_car_data(self.get_live_data())
            car_simulation.move(
                {
                    "movement_instructions": {
                        "speed_instruction": speed_instruction,
                        "turn_instruction": turn_instruction,
                    },
                    "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
                }
            )
            return track.get_distance_to_point(car_simulation.front_middle)

        if self.velocity == 0:
            return TurnInstruction.NO_CHANGE
        return min(TurnInstruction, key=_distance_to_track_after_instruction)
