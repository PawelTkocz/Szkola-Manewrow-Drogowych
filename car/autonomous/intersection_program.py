from abc import ABC, abstractmethod
from car.autonomous.program import MovementDecision
from car.autonomous.schemas import IntersectionManoeuvreDescription
from car.autonomous.track_follower import TrackFollower
from car.car import LiveCarData
from car.model import CarModel
from manoeuvres.intersection_manoeuvre import IntersectionManoeuvre


class IntersectionProgram(ABC):
    def __init__(self, track_follower: TrackFollower):
        self.track_follower = track_follower
        self.current_manoeuvre: IntersectionManoeuvre | None = None

    @abstractmethod
    def prepare_manoeuvre(self, model: CarModel, manoeuvre_description: IntersectionManoeuvreDescription) -> IntersectionManoeuvre:
        pass

    @abstractmethod
    def make_movement_decision(self, live_car_data: LiveCarData) -> MovementDecision:
        pass