from car.autonomous.program import AutonomousDrivingProgram, MovementDecision
from car.car import Car, RoadSegment, SpeedModifications
from car.model import CarModel
from geometry import Direction, Directions, Point
from intersection.intersection import Intersection
from manoeuvres.manoeuvre import Manoeuvre

class AutonomousCar(Car):
    def __init__(
        self,
        model: CarModel,
        color: str,
        front_middle_position: Point,
        road_segment: RoadSegment,
        autonomous_driving_program: AutonomousDrivingProgram, 
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
    ):
        super().__init__(model, color, front_middle_position, road_segment, direction, velocity)
        self.autonomous_driving_program = autonomous_driving_program

    def set_manoeuvre(self, manoeuvre: Manoeuvre):
        self.autonomous_driving_program.set_manoeuvre(manoeuvre)
        # check if it is defined for current_road_segment (for examply by road_segment_id)

    def move(self, *, movement_decision: MovementDecision | None = None):
        movement_decision = movement_decision or self.autonomous_driving_program.make_movement_decision(self._live_car_data)
        self.apply_movement_decision(movement_decision)
        super().move()
        return movement_decision

    def apply_movement_decision(self, movement_decision: MovementDecision):
        self._apply_speed_modification(movement_decision['speed_modification'])
        self.turn(movement_decision['turn_direction'])

    def _apply_speed_modification(self, modification: SpeedModifications):
        if modification == SpeedModifications.SPEED_UP:
            direction = Directions.FRONT if self.velocity >= 0 else Directions.BACK
            self.speed_up(direction)
        elif modification == SpeedModifications.NO_CHANGE:
            pass
        elif modification == SpeedModifications.BRAKE:
            self.brake()