
from abc import ABC
from enum import Enum
from typing import TypedDict

from car.autonomous.intersection_program import IntersectionManoeuvreDescription, IntersectionProgram
from car.car import LiveCarData, SpeedModifications
from car.model import CarModel
from geometry import Directions
from intersection.intersection import Intersection
from manoeuvres.intersection_manoeuvre import IntersectionManoeuvre
from manoeuvres.manoeuvre import Manoeuvre

class AvailableManoeuvres(Enum):
    INTERSECTION = 1
    ROUNDABOUT = 2

class MovementDecision(TypedDict):
    speed_modification: SpeedModifications
    turn_direction: Directions

class AutonomousDrivingProgram(ABC):
    def __init__(
        self,
        model: CarModel,
        intersection_program: IntersectionProgram,
        roundabout_program: IntersectionProgram
    ):
        self.model = model
        self.intersection_program = intersection_program
        self.manoeuvres_programs = {
            AvailableManoeuvres.INTERSECTION: intersection_program,
            AvailableManoeuvres.ROUNDABOUT: roundabout_program,
        }
        self.current_manoeuvre: AvailableManoeuvres | None = None

    def set_manoeuvre(self, manoeuvre_description: IntersectionManoeuvreDescription):
        manoeuvre_name = manoeuvre_description['name']
        self.current_manoeuvre = manoeuvre_name
        manoeuvre_program = self.manoeuvres_programs[manoeuvre_name]
        manoeuvre_program.prepare_manoeuvre(manoeuvre_description)

    def make_movement_decision(self, live_car_data: LiveCarData) -> MovementDecision:
        if self.current_manoeuvre is None:
            return {"speed_modification": SpeedModifications.NO_CHANGE, "turn_direction": Directions.FRONT}
        manoeuvre_program = self.manoeuvres_programs[self.current_manoeuvre]
        return manoeuvre_program.make_movement_decision(live_car_data)