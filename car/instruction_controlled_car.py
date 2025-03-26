from enum import Enum
from typing import TypedDict
from car.car import Car
from car.model import CarModel
from geometry import Direction, Directions, Point


class SpeedModifications(Enum):
    SPEED_UP = 1
    NO_CHANGE = 2
    BRAKE = 3


class MovementInstruction(TypedDict):
    speed_modification: SpeedModifications
    turn_direction: Directions  # create separate enum


class InstructionControlledCar(Car):
    def __init__(
        self,
        registry_number: str,
        model: CarModel,
        color: str,
        front_middle_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
    ):
        super().__init__(
            registry_number, model, color, front_middle_position, direction, velocity
        )

    def apply_movement_instruction(self, movement_instruction: MovementInstruction):
        self._apply_speed_modification(movement_instruction["speed_modification"])
        self.turn(movement_instruction["turn_direction"])

    def _apply_speed_modification(self, modification: SpeedModifications):
        if modification == SpeedModifications.SPEED_UP:
            direction = Directions.FRONT if self.velocity >= 0 else Directions.BACK
            self.speed_up(direction)
        elif modification == SpeedModifications.NO_CHANGE:
            pass
        elif modification == SpeedModifications.BRAKE:
            self.brake()
