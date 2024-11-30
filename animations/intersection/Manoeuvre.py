from animations.intersection.ManoeuvrePhase import ManoeuvrePhase
from cars.Car import Car


class Manoeuvre:
    """
    Class representing manoeuvre
    """

    def __init__(self, phases: list[ManoeuvrePhase]):
        self.phases = phases
        self.current_phase_index = 0

    def current_track(self):
        return self.phases[self.current_phase_index].track

    def current_non_preference_zone(self):
        return self.phases[self.current_phase_index].non_preperence_zone
