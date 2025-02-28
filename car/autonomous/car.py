from car.autonomous.program import MovementDecision
from car.car import Car, SpeedModifications
from car.model import CarModel
from geometry import Direction, Directions, Point
from manoeuvres.manoeuvre import Manoeuvre

# jedna klasa musi byc odpowiedzialna za opisanie sytuacji na skrzyzowaniu:
# jakie samochody biora udzial, kto kumu musi ustapic pierwszenstwa

# inna klasa musi byc odpowiedzialna za opisanie co dokladnie dany samochod ma zrobic, krok po kroku

# klasa z intersection state = pozycja samochodow, to skad startowaly, ewentualna sygnalizacja swietlna stan, znaki


class AutonomousCar(Car):
    def __init__(
        self,
        model: CarModel,
        color: str,
        front_middle_position: Point,
        autonomous_driving_program,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
    ):
        super().__init__(model, color, front_middle_position, direction, velocity)
        self.autonomous_driving_program = autonomous_driving_program

    def set_manoeuvre(self, manoeuvre: Manoeuvre):
        self.current_manoeuvre = manoeuvre

    def move(self, *, movement_decision: MovementDecision | None = None):
        movement_decision = movement_decision or self.autonomous_driving_program()
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