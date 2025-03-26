from manoeuvres.manoeuvre_phase import ManoeuvrePhase
from traffic_control_center.schemas import LiveCarData


class Manoeuvre:
    """
    Class representing manoeuvre
    """

    def __init__(self, phases: list[ManoeuvrePhase]):
        self.phases = phases

    def current_phase_index(self, phase_index: int, live_car_data: LiveCarData) -> int:
        if self.phases[phase_index].is_phase_over(
            live_car_data["front_middle"], live_car_data["velocity"]
        ):
            return phase_index + 1
        return phase_index
