from enum import Enum
from typing import TypedDict
from car.car import Car
from car.model import CarModel
from geometry import Direction, Directions, Point


class SpeedInstruction(Enum):
    ACCELERATE_FRONT = "ACCELERATE_FRONT"
    NO_CHANGE = "NO_CHANGE"
    BRAKE = "BRAKE"
    ACCELERATE_REVERSE = "ACCELERATE_REVERSE"


class TurnInstruction(Enum):
    TURN_LEFT = "TURN_LEFT"
    NO_CHANGE = "NO_CHANGE"
    TURN_RIGHT = "TURN_RIGHT"


class CarControlInstructions(TypedDict):
    speed_instruction: SpeedInstruction
    turn_instruction: TurnInstruction


class InstructionControlledCar(Car):
    def __init__(
        self,
        registry_number: str,
        model: CarModel,
        color: str,
        front_middle_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
        wheels_direction: Direction = Direction(Point(1, 0)),
    ):
        super().__init__(
            registry_number,
            model,
            color,
            front_middle_position,
            direction,
            velocity,
            wheels_direction,
        )

    def move(self, control_instructions: CarControlInstructions | None = None) -> None:
        if control_instructions:
            self.apply_control_instructions(control_instructions)
        super().move()

    def apply_control_instructions(
        self, control_instructions: CarControlInstructions
    ) -> None:
        self._apply_speed_instruction(control_instructions["speed_instruction"])
        self._apply_turn_instruction(control_instructions["turn_instruction"])

    def _apply_speed_instruction(self, speed_instruction: SpeedInstruction) -> None:
        if speed_instruction == SpeedInstruction.ACCELERATE_FRONT:
            self.accelerate(Directions.FRONT)
        elif speed_instruction == SpeedInstruction.NO_CHANGE:
            pass
        elif speed_instruction == SpeedInstruction.BRAKE:
            self.brake()
        elif speed_instruction == SpeedInstruction.ACCELERATE_REVERSE:
            self.accelerate(Directions.BACK)

    def _apply_turn_instruction(self, turn_instruction: TurnInstruction) -> None:
        if turn_instruction == TurnInstruction.TURN_LEFT:
            self.turn_left()
        elif turn_instruction == TurnInstruction.NO_CHANGE:
            pass
        elif turn_instruction == TurnInstruction.TURN_RIGHT:
            self.turn_right()
