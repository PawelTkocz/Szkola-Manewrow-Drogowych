from autonomousDriving.BasicAutonomousDriving import BasicAutonomousDriving
from autonomousDriving.Track import Track
from cars.Car import Car


class ManoeuvrePhase:
    """
    Class representing one phase of a manoeuvre
    """

    def __init__(self, track: Track):
        self.track = track

    def move(self, autonomous_driving: BasicAutonomousDriving, other_cars: list[Car]):
        # cars_with_preference = get_cars_with_preference(self.car, cars)
        pass

    def is_phase_over(self):
