from enum import Enum
from typing import TypedDict
from car.car import Car
from car.model import CarModel
from car.schemas import GearboxState
from geometry import Direction, Point


class SpeedInstruction(Enum):
    ACCELERATE = "ACCELERATE"
    NO_CHANGE = "NO_CHANGE"
    BRAKE = "BRAKE"


class TurnInstruction(Enum):
    TURN_LEFT = "TURN_LEFT"
    NO_CHANGE = "NO_CHANGE"
    TURN_RIGHT = "TURN_RIGHT"


class CarControlInstructions(TypedDict):
    speed_instruction: SpeedInstruction
    turn_instruction: TurnInstruction
    gearbox_instruction: GearboxState


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

    def apply_control_instructions(self, control_instructions: CarControlInstructions):
        self._apply_gearbox_instruction(control_instructions["gearbox_instruction"])
        self._apply_speed_instruction(control_instructions["speed_instruction"])
        self._apply_turn_instruction(control_instructions["turn_instruction"])

    def _apply_gearbox_instruction(self, gearbox_instruction: GearboxState) -> None:
        self.shift_gear(gearbox_instruction)

    def _apply_speed_instruction(self, speed_instruction: SpeedInstruction):
        if speed_instruction == SpeedInstruction.ACCELERATE:
            self.accelerate()
        elif speed_instruction == SpeedInstruction.NO_CHANGE:
            pass
        elif speed_instruction == SpeedInstruction.BRAKE:
            self.brake()

    def _apply_turn_instruction(self, turn_instruction: TurnInstruction) -> None:
        if turn_instruction == TurnInstruction.TURN_LEFT:
            self.turn_left()
        elif turn_instruction == TurnInstruction.NO_CHANGE:
            pass
        elif turn_instruction == TurnInstruction.TURN_RIGHT:
            self.turn_right()
