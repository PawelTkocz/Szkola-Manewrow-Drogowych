
from abc import ABC, abstractmethod

from car.autonomous.intersection_program import IntersectionProgram
from car.autonomous.schemas import IntersectionManoeuvreDescription, Manoeuvre, ManoeuvreDescription
from car.autonomous.track_follower import MovementDecision
from car.car import LiveCarData

class AutonomousDrivingProgram(ABC):
    def __init__(
        self,
        name: str,
        intersection_program: IntersectionProgram,
    ):
        self.name = name
        self.intersection_program = intersection_program
        self.current_manoeuvre_description: ManoeuvreDescription | None = None
        self.current_manoeuvre: Manoeuvre | None = None

    def set_manoeuvre(self, manoeuvre_description: ManoeuvreDescription):
        self.current_manoeuvre = manoeuvre_description
        if isinstance(manoeuvre_description, IntersectionManoeuvreDescription):
            self.current_manoeuvre = self.intersection_program.prepare_manoeuvre(manoeuvre_description)

    @abstractmethod
    def make_movement_decision(self, live_car_data: LiveCarData) -> MovementDecision:
        pass