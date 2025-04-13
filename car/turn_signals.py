from schemas import HorizontalDirection


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
    def __init__(
        self, tick_interval: int, activated_turn_signal: HorizontalDirection | None
    ) -> None:
        self.turn_signals = {
            horizontal_direction: TurnSignal(
                tick_interval, activated_turn_signal == horizontal_direction
            )
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

    def are_turn_signals_lights_on(self) -> dict[HorizontalDirection, bool]:
        return {
            horizontal_direction: self.turn_signals[
                horizontal_direction
            ].is_turn_signal_light_on()
            for horizontal_direction in HorizontalDirection
        }
