from manoeuvres.manoeuvre_phase import ManoeuvrePhase
from smart_city.schemas import LiveCarData


class Manoeuvre:
    """
    Class representing manoeuvre
    """

    def __init__(self, phases: list[ManoeuvrePhase]):
        self.phases = phases
        self.current_phase_index = 0

    def get_current_phase(self) -> ManoeuvrePhase | None:
        return (
            self.phases[self.current_phase_index]
            if self.current_phase_index < len(self.phases)
            else None
        )

    def update_current_phase(self, live_car_data: LiveCarData) -> None:
        current_phase = self.get_current_phase()
        if not current_phase:
            return
        if current_phase.is_phase_over(
            live_car_data["live_state"]["front_middle"],
            live_car_data["live_state"]["velocity"],
        ):
            self.current_phase_index += 1
