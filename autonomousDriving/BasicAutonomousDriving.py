from Geometry import Directions, Rectangle, calculate_line, distance_of_point_to_line
from animations.intersection.Manoeuvre import Manoeuvre
from autonomousDriving.CarSimulation import CarSimulation
from car.Car import Car, SpeedModifications


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


def dont_speed_up_if_will_go_off_track(
    car_simulation: CarSimulation,
    max_distance_to_track,
    max_steps_into_future,
    turning_policy,
):
    for speed_modification in [
        SpeedModifications.SPEED_UP,
        SpeedModifications.NO_CHANGE,
    ]:
        start_state = car_simulation.get_state()
        car_simulation.apply_speed_modification(speed_modification)
        car_simulation.move()
        will_go_off_track = car_simulation.will_go_off_track(
            max_distance_to_track,
            max_steps_into_future,
            turning_policy,
        )
        car_simulation.set_state(start_state)
        if not will_go_off_track:
            return speed_modification
    return SpeedModifications.BRAKE


def hold_to_track_with_preference(
    car_simulation: CarSimulation,
    max_distance_to_track,
    max_steps_into_future,
    turning_policy,
    simulation_speed_policy,
    non_preference_zone,
    cars: list["CarSimulation"],
):
    for speed_modification in [
        SpeedModifications.SPEED_UP,
        SpeedModifications.NO_CHANGE,
    ]:
        start_state = car_simulation.get_state()
        car_simulation.apply_speed_modification(speed_modification)
        car_simulation.move()
        will_go_off_track = car_simulation.will_go_off_track(
            max_distance_to_track,
            1,
            turning_policy,
        )
        will_collide = car_simulation.will_collide(
            max_steps_into_future,
            turning_policy,
            non_preference_zone,
        )
        car_simulation.set_state(start_state)
        if not will_go_off_track and not will_collide:
            return speed_modification
        if will_go_off_track:
            continue
        # will collide
        # check if you can escape non preference zone without collisions
        # return SpeedModifications.BRAKE
        # return SpeedModifications.NO_CHANGE
        # to juz jest po set_state(start_state) wiec dla wszystkich speed mod wynik ten sam
        if len(cars) == 0 or not car_simulation.will_violate_the_right_of_way(
            turning_policy, simulation_speed_policy, non_preference_zone, cars
        ):
            return speed_modification
    return SpeedModifications.BRAKE


class BasicAutonomousDriving:
    def __init__(self, car: Car, manoeuvre: Manoeuvre):
        self.car = car
        self.manoeuvre = manoeuvre
        self.car_simulation = CarSimulation(car, self.manoeuvre.current_track())
        self.turning_policy = closest_to_track_turning_policy
        self.max_distance_to_track = 10
        self.max_steps_into_future = 40  # 340 max speed / resistance
        self.simulation_speed_policy = (
            lambda car_simulation: dont_speed_up_if_will_go_off_track(
                car_simulation, self.max_distance_to_track, 1, self.turning_policy
            )
        )
        self.speed_policy = lambda car_simulation, cars: hold_to_track_with_preference(
            car_simulation,
            self.max_distance_to_track,
            self.max_steps_into_future,
            self.turning_policy,
            self.simulation_speed_policy,
            self.manoeuvre.current_non_preference_zone(),
            cars,
        )

    def move(self, cars: list[CarSimulation]):
        # z jakiegos powodu po jakims czasie zastosowywanie analogicznych zmian w predkosci i skrecaniu dla car i car_simulation
        # ich wspolrzedne corners zaczynaja sie roznic na ostatnich cyfrach po przecinku (np 10) wiec byc moze warto kopiowac a
        # nie zakladac ze zawsze beda rowne

        best_turn_direction = self.turning_policy(self.car_simulation)
        best_speed_modification = self.speed_policy(self.car_simulation, cars)
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
