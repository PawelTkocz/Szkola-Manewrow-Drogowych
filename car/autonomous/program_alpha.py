from car.autonomous.intersection_program_alpha import IntersectionProgramAlpha
from car.autonomous.program import AutonomousDrivingProgram
from car.autonomous.schemas import IntersectionManoeuvreDescription
from car.autonomous.track_follower import MovementDecision
from car.car import SpeedModifications
from car.schemas import LiveCarData
from geometry import Directions


class AutnomousDrivingProgramAlpha(AutonomousDrivingProgram):
    intersection_program = IntersectionProgramAlpha()
    name = "alpha_program_1.0"

    def __init__(self):
        super().__init__(self.name, self.intersection_program)

    def make_movement_decision(self, live_car_data: LiveCarData) -> MovementDecision:
        if self.current_manoeuvre is None:
            return {"speed_modification": SpeedModifications.NO_CHANGE, "turn_direction": Directions.FRONT}
        if isinstance(self.current_manoeuvre, IntersectionManoeuvreDescription):
            return self.intersection_program.make_movement_decision(live_car_data)
        return {"speed_modification": SpeedModifications.NO_CHANGE, "turn_direction": Directions.FRONT}