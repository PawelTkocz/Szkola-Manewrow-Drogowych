
from typing import TypedDict

from car.autonomous.intersection_program import IntersectionProgram
from car.car import SpeedModifications
from car.model import CarModel
from geometry import Directions
from manoeuvres.manoeuvre import Manoeuvre


class MovementDecision(TypedDict):
    speed_modification: SpeedModifications
    turn_direction: Directions

class ManoeuvresPrograms(TypedDict):
    intersection: IntersectionProgram

class AutonomousDrivingProgram():
    def __init__(
        self,
        model: CarModel,
        manoeuvres_programs: ManoeuvresPrograms
    ):
        self.model = model
        self.manoeuvres_programs = manoeuvres_programs

    def set_manoeuvre(self, manoeuvre_name: str, car_manoeuvre: Manoeuvre, manoeuvre_data):
        self.current_manoeuvre = self.manoeuvres_programs.get(manoeuvre_name)

    def make_movement_decision(self, live_car_data, car_ma):
        pass

# program should have TrackFollower() field and then pass it as parameter to IntersectionProgram and other manoeuvre specific programs