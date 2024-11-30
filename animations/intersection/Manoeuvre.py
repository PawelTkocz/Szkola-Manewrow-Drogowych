from animations.intersection.ManoeuvrePhase import ManoeuvrePhase
from cars.Car import Car


class Manoeuvre:
    """
    Class representing manoeuvre
    """

    def __init__(self, phases: list[ManoeuvrePhase]):
        self.phases = phases
        self.current_phase_index = 0

    def move(self, car: Car, other_cars: list[Car]):
        self.phases[self.current_phase_index].move(car, other_cars)
