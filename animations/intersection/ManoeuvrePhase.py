from Geometry import Rectangle
from autonomousDriving.Track import Track
from cars.Car import Car


class ManoeuvrePhase:
    """
    Class representing one phase of a manoeuvre
    """

    def __init__(self, track: Track, non_preference_zone: Rectangle):
        self.track = track
        self.non_preperence_zone = non_preference_zone

    def is_phase_over(self):
        pass
