from Geometry import Directions, Rectangle, calculate_line, distance_of_point_to_line
from animations.intersection.Manoeuvre import Manoeuvre
from autonomousDriving.CarSimulation import CarSimulation
from cars.Car import Car, SpeedModifications


def closest_to_track_turning_policy(car_simulation: CarSimulation):
    min_distance = None
    best_turn_direction = None

    for turn_direction in [Directions.FRONT, Directions.LEFT, Directions.RIGHT]:
        start_state = car_simulation.get_state()
        car_simulation.turn(turn_direction)
        car_simulation.move()
        distance = car_simulation.find_distance_to_track()
        if min_distance is None or distance < min_distance:
            best_turn_direction = turn_direction
            min_distance = distance
        car_simulation.set_state(start_state)

    return best_turn_direction


def straight_lines_turning_policy(car_simulation: CarSimulation):
    min_distance = None
    best_turn_direction = None

    closest_point_on_track_index = car_simulation.find_index_of_closest_point_on_track()
    straight_line_end_point = car_simulation.find_straight_line_end_point_on_track(
        closest_point_on_track_index
    )

    for turn_direction in [Directions.FRONT, Directions.LEFT, Directions.RIGHT]:
        start_state = car_simulation.get_state()
        car_simulation.turn(turn_direction)
        car_simulation.move()
        distance = car_simulation.find_distance_to_point(straight_line_end_point)
        if min_distance is None or distance < min_distance:
            best_turn_direction = turn_direction
            min_distance = distance
        car_simulation.set_state(start_state)

    return best_turn_direction


class BasicAutonomousDriving:
    def __init__(self, car: Car, manoeuvre: Manoeuvre):
        self.car = car
        self.manoeuvre = manoeuvre
        self.car_simulation = CarSimulation(car, self.manoeuvre.current_track())
        self.turning_policy = closest_to_track_turning_policy
        self.max_distance_to_track = 10
        self.max_steps_into_future = 50  # 340 max speed / resistance

    def find_best_speed_modification(self):
        for speed_modification in [
            SpeedModifications.SPEED_UP,
            SpeedModifications.NO_CHANGE,
        ]:
            start_state = self.car_simulation.get_state()
            self.car_simulation.apply_speed_modification(speed_modification)
            self.car_simulation.move()
            will_go_off_track = self.car_simulation.will_go_off_track(
                self.max_distance_to_track,
                1,
                self.turning_policy,
                None,
            )
            will_collide = self.car_simulation.will_collide(
                self.max_steps_into_future,
                self.turning_policy,
                self.manoeuvre.current_non_preference_zone(),
            )
            self.car_simulation.set_state(start_state)
            if not will_go_off_track and not will_collide:
                return speed_modification
        return SpeedModifications.BRAKE

    def move(self, cars: list[Car]):
        # z jakiegos powodu po jakims czasie zastosowywanie analogicznych zmian w predkosci i skrecaniu dla car i car_simulation
        # ich wspolrzedne corners zaczynaja sie roznic na ostatnich cyfrach po przecinku (np 10) wiec byc moze warto kopiowac a
        # nie zakladac ze zawsze beda rowne

        best_turn_direction = self.turning_policy(self.car_simulation)
        best_speed_modification = self.find_best_speed_modification()
        self.apply_best_changes(best_turn_direction, best_speed_modification)
        return best_turn_direction, best_speed_modification

    def apply_best_changes(
        self, turn_direction: Directions, speed_modification: SpeedModifications
    ):
        self.car_simulation.turn(turn_direction)
        self.car_simulation.apply_speed_modification(speed_modification)
        self.car_simulation.move()

        self.car.turn(turn_direction)
        self.car.apply_speed_modification(speed_modification)
        self.car.move()
