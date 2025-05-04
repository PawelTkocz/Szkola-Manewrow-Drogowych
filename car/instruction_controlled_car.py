from enum import Enum
from typing import TypedDict
from car.car import Car
from car.schemas import AccelerationDirection
from schemas import HorizontalDirection


class SpeedInstruction(Enum):
    ACCELERATE_FORWARD = "ACCELERATE_FRONT"
    NO_CHANGE = "NO_CHANGE"
    BRAKE = "BRAKE"
    ACCELERATE_REVERSE = "ACCELERATE_REVERSE"


class TurnInstruction(Enum):
    TURN_LEFT = "TURN_LEFT"
    NO_CHANGE = "NO_CHANGE"
    TURN_RIGHT = "TURN_RIGHT"


class TurnSignalsInstruction(Enum):
    LEFT_SIGNAL_ON = "LEFT_SIGNAL_ON"
    NO_SIGNALS_ON = "NO_SIGNALS_ON"
    RIGHT_SIGNAL_ON = "RIGHT_SIGNAL_ON"


class CarMovementInstructions(TypedDict):
    speed_instruction: SpeedInstruction
    turn_instruction: TurnInstruction


class CarControlInstructions(TypedDict):
    movement_instructions: CarMovementInstructions
    turn_signals_instruction: TurnSignalsInstruction


class InstructionControlledCar(Car):
    def apply_control_instructions(
        self, control_instructions: CarControlInstructions
    ) -> None:
        self._apply_movement_instructions(control_instructions["movement_instructions"])
        self._apply_turn_signal_instruction(
            control_instructions["turn_signals_instruction"]
        )

    def _apply_movement_instructions(
        self, movement_instruction: CarMovementInstructions
    ) -> None:
        self._apply_speed_instruction(movement_instruction["speed_instruction"])
        self._apply_turn_instruction(movement_instruction["turn_instruction"])

    def _apply_speed_instruction(self, speed_instruction: SpeedInstruction) -> None:
        if speed_instruction == SpeedInstruction.ACCELERATE_FORWARD:
            self.accelerate(AccelerationDirection.FORWARD)
        elif speed_instruction == SpeedInstruction.NO_CHANGE:
            pass
        elif speed_instruction == SpeedInstruction.BRAKE:
            self.brake()
        elif speed_instruction == SpeedInstruction.ACCELERATE_REVERSE:
            self.accelerate(AccelerationDirection.REVERSE)

    def _apply_turn_instruction(self, turn_instruction: TurnInstruction) -> None:
        if turn_instruction == TurnInstruction.TURN_LEFT:
            self.turn(HorizontalDirection.LEFT)
        elif turn_instruction == TurnInstruction.NO_CHANGE:
            pass
        elif turn_instruction == TurnInstruction.TURN_RIGHT:
            self.turn(HorizontalDirection.RIGHT)

    def _apply_turn_signal_instruction(
        self, turn_signal_instruction: TurnSignalsInstruction
    ) -> None:
        if turn_signal_instruction == TurnSignalsInstruction.NO_SIGNALS_ON:
            self.deactivate_turn_signal()
        elif turn_signal_instruction == TurnSignalsInstruction.LEFT_SIGNAL_ON:
            self.activate_turn_signal(HorizontalDirection.LEFT)
        elif turn_signal_instruction == TurnSignalsInstruction.RIGHT_SIGNAL_ON:
            self.activate_turn_signal(HorizontalDirection.RIGHT)
