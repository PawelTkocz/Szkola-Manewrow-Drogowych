from enum import Enum
from schemas import HorizontalDirection


class TurnSignalType(Enum):
    RIGHT_SIGNAL = "right_signal"
    NO_SIGNAL = "no_signal"
    LEFT_SIGNAL = "left_signal"


class TurnSignal:
    def __init__(self, tick_interval: int, activated: bool = False) -> None:
        self.tick_interval = tick_interval
        self.activated = activated
        self.ticks_counter = 0

    def activate(self) -> None:
        if self.activated:
            return
        self.activated = True
        self.ticks_counter = 0

    def deactivate(self) -> None:
        self.activated = False

    def is_turn_signal_light_on(self) -> bool:
        return self.activated and (self.ticks_counter // self.tick_interval) % 2 == 0

    def tick(self) -> None:
        self.ticks_counter += 1


class TurnSignals:
    def __init__(self, tick_interval: int) -> None:
        self.turn_signals = {
            horizontal_direction: TurnSignal(tick_interval)
            for horizontal_direction in HorizontalDirection
        }

    def activate(self, turn_signal_side: HorizontalDirection) -> None:
        self.turn_signals[turn_signal_side].activate()

    def deactivate(self) -> None:
        for turn_signal in self.turn_signals.values():
            turn_signal.deactivate()

    def tick(self) -> None:
        for turn_signal in self.turn_signals.values():
            turn_signal.tick()

    def is_turn_signal_light_on(self, side: HorizontalDirection) -> bool:
        return self.turn_signals[side].is_turn_signal_light_on()

    @property
    def turn_signal(self) -> TurnSignalType:
        if self.turn_signals[HorizontalDirection.LEFT].activated:
            return TurnSignalType.LEFT_SIGNAL
        if self.turn_signals[HorizontalDirection.RIGHT].activated:
            return TurnSignalType.RIGHT_SIGNAL
        return TurnSignalType.NO_SIGNAL
