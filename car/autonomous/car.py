from car.autonomous.program import MovementDecision
from car.car import Car
from car.model import CarModel
from geometry import Direction, Point
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
        if movement_decision:
            speed_modification = movement_decision['speed_modification']
            turn_direction = movement_decision['turn_direction']
        else:
            turn_direction, speed_modification = self.autonomous_driving_program()
        self.apply_speed_modification(speed_modification)
        self.turn(turn_direction)
        super().move()

    def apply_movement_decision(self, movement_decision: MovementDecision):
        pass
        # think about moving here the function from car class with apply_speed_modification
