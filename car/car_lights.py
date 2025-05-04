from car.car_part import CarPart
from car.model import LightsSpecification
from car.schemas import CarPartPosition, LightsColors
from car.turn_signals import TurnSignalType, TurnSignals
from geometry.direction import Direction
from geometry.vector import Point
from schemas import HorizontalDirection


class CarLight(CarPart):
    def __init__(
        self,
        position: CarPartPosition,
        color: str,
        car_front_middle: Point,
        car_direction: Direction,
    ) -> None:
        super().__init__(position, color, car_front_middle, car_direction)

    def set_color(self, color: str) -> None:
        self.color = color


class CarLights:
    def __init__(
        self,
        specification: LightsSpecification,
        colors: LightsColors,
        car_front_middle: Point,
        car_direction: Direction,
    ) -> None:
        self.left_light = CarLight(
            specification["left"],
            colors["default"],
            car_front_middle,
            car_direction,
        )
        self.right_light = CarLight(
            specification["right"],
            colors["default"],
            car_front_middle,
            car_direction,
        )
        self.turn_signals = TurnSignals(specification["turn_signals_tick_interval"])
        self.color = colors["default"]
        self.turn_signal_color = colors["turn_signal"]

    def activate_turn_signal(self, turn_signal_side: HorizontalDirection) -> None:
        self.turn_signals.activate(turn_signal_side)

    def deactivate_turn_signal(self) -> None:
        self.turn_signals.deactivate()

    @property
    def turn_signal(self) -> TurnSignalType:
        return self.turn_signals.turn_signal

    def tick(self) -> None:
        self.turn_signals.tick()
        for side, light in [
            (HorizontalDirection.LEFT, self.left_light),
            (HorizontalDirection.RIGHT, self.right_light),
        ]:
            if self.turn_signals.is_turn_signal_light_on(side):
                light.set_color(self.turn_signal_color)
            else:
                light.set_color(self.color)
