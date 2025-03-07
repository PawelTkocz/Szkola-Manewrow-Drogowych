from car.car import LiveCarData
from manoeuvres.manoeuvre_phase import ManoeuvrePhase


class Manoeuvre:
    """
    Class representing manoeuvre
    """

    def __init__(self, phases: list[ManoeuvrePhase]):
        self.phases = phases
        self.current_phase_index = 0

    def current_phase(self):
        return self.phases[self.current_phase_index]
    
    def update_current_phase(self, live_car_data: LiveCarData) -> bool:
        if self.phases[self.current_phase_index].is_phase_over(live_car_data["front_middle"], live_car_data["velocity"]):
            self.current_phase_index += 1
            return True
        return False