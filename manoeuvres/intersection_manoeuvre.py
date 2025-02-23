from animations.intersection.manoeuvre_phase import ManoeuvrePhase
from autonomousDriving.track import Track
from car.car import Car


class IntersectionManoeuvre(ManoeuvrePhase):
    """
    Class representing one phase of a manoeuvre
    """

    def __init__(self, track: Track, non_preference_zone):
        super().__init__(track, non_preference_zone)

    def move(self, car: Car, other_cars: list[Car]):
        # cars_with_preference = get_cars_with_preference(self.car, cars)
        pass

    def is_phase_over(self):
        pass


# przyspieszaj dopoki dojedziesz do punktu A, takiego ze hamujac zdazysz sie zatrzymac przed wjazdem na skrzyzowanie
# w tym punkcie rozwaz wszystkie samochody, ktorym musisz ustapic pierwszenstwa
# sprawdz, czy zdazysz opuscic skrzyzowanie zanim ktorykolwiek z nich dojedzie do skrzyzowania
# jesli tak - jedziemy dalej
# jesli nie - zaczynamy hamowanie, tak zeby zdazyc wyhamowac przed skrzyzowaniem, obliczamy po jakim czasie
# samochody z pierwszenstwem opuszcza skrzyzowanie i znowu sprawdzamy czy zdazymy przejechac zanim cos nowego nadjedzie
