from typing import TypedDict


class CarControlInstructionsJSON(TypedDict):
    speed_instruction: str
    turn_instruction: str
    turn_signals_instruction: str
