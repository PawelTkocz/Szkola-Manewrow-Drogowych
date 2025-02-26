from car.autonomous.track import Track, TrackPath
from car.car_state import CarState
from geometry import Directions
from intersection.intersection import Intersection

vertical = [Directions.UP, Directions.DOWN]
horizontal = [Directions.LEFT, Directions.RIGHT]
directions = [Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT]


class IntersectionProgram:
    def __init__(self, car_state: CarState):
        self.car_state = car_state
        self.intersection = None
        self.starting_side = None
        self.ending_side = None
        self.track_path = None
        self._track = Track()

    def prepare_for_manoeuvre(
        self,
        intersection: Intersection,
        starting_side: Directions,
        ending_side: Directions,
    ):
        self.intersection = intersection
        self.starting_side = starting_side
        self.ending_side = ending_side
        self.track = self._calculate_track()

    def _calculate_turn_track(
        self, turn_direction: Directions, turn_margin: float, turn_sharpness: float
    ) -> TrackPath:
        car_length = self.car_state.length
        incoming_line = self.intersection.intersection_parts["incoming_lines"][
            self.starting_side
        ]
        start_point = incoming_line.rear_middle
        outcoming_line = self.intersection.intersection_parts["outcoming_lines"][
            self.ending_side
        ]
        end_point = outcoming_line.front_middle.add_vector(
            outcoming_line.direction.scale_to_len(car_length)
        )
        turn_start_point = incoming_line.front_middle.add_vector(
            incoming_line.direction.get_negative_of_a_vector().scale_to_len(turn_margin)
        )
        turn_end_point = outcoming_line.rear_middle.add_vector(
            outcoming_line.direction.scale_to_len(turn_margin)
        )
        incoming_track_path = self._track.get_straight_track(
            start_point, turn_start_point
        )
        turning_track_path = self._track.get_right_angle_turn(
            turn_start_point, turn_end_point, turn_direction, turn_sharpness
        )
        outcoming_track_path = self._track.get_straight_track(turn_end_point, end_point)
        return incoming_track_path + turning_track_path + outcoming_track_path

    def _calculate_left_turn_track(self):
        return self._calculate_turn_track(Directions.LEFT, 0, 0.66)

    def _calculate_right_turn_track(self):
        return self._calculate_turn_track(Directions.RIGHT, self.car_state.length, 0.66)

    def _calculate_straight_track(self):
        car_length = self.car_state.length
        start_point = self.intersection.intersection_parts["incoming_lines"][
            self.starting_side
        ].rear_middle
        outcoming_line = self.intersection.intersection_parts["outcoming_lines"][
            self.ending_side
        ]
        end_point = outcoming_line.front_middle.add_vector(
            outcoming_line.direction.scale_to_len(car_length)
        )
        return self._track.get_straight_track(start_point, end_point)

    def _calculate_track(self) -> TrackPath:
        if (self.starting_side in vertical and self.ending_side in vertical) or (
            self.starting_side in horizontal and self.ending_side in horizontal
        ):
            return self._calculate_vertical_track()

        starting_side_index = directions.index(self.starting_side)
        if directions[(starting_side_index + 1) % 4] == self.ending_side:
            return self._calculate_left_turn_track()
        else:
            return self._calculate_right_turn_track()

    def make_movement_decision(self):
        if not self.intersection or not self.starting_side or not self.ending_side:
            return (None, None)
        cars_on_intersection = self.intersection.cars
        # make some decision
        return None, None


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

    def will_violate_the_right_of_way(
        self,
        turning_policy,
        speed_policy,
        non_preference_zone: Rectangle,
        cars: list["CarSimulation"],
    ):
        if self.body.collides(non_preference_zone) and any(
            car.body.collides(non_preference_zone) for car in cars
        ):
            return True
        self_start_state = self.get_state()
        cars_state = [car.get_state() for car in cars]
        collides = False
        cnt = 0
        entered_non_preference_zone = False
        while True:  # trzeba naprawic
            cnt += 1
            turn_direction = turning_policy(self)  # better pass state instead of self
            speed_modification = speed_policy(self)
            self.turn(turn_direction)
            self.apply_speed_modification(speed_modification)
            self.move()

            for car in cars:
                turn_direction = turning_policy(
                    car
                )  # better pass state instead of self
                speed_modification = speed_policy(car)
                car.turn(turn_direction)
                car.apply_speed_modification(speed_modification)
                car.move()

            if self.body.collides(non_preference_zone) and any(
                car.body.collides(non_preference_zone) for car in cars
            ):
                collides = True
                break
            if self.body.collides(non_preference_zone):
                entered_non_preference_zone = True
            elif entered_non_preference_zone:
                break
        self.set_state(self_start_state)
        for index, car in enumerate(cars):
            car.set_state(cars_state[index])
        return collides
    
    def will_collide(self, max_steps_into_future: int, turning_policy, obj: Rectangle):
        if self.collides(obj):
            return True
        start_state = self.get_state()
        collides = False
        for _ in range(max_steps_into_future):
            turn_direction = turning_policy(self)  # better pass state instead of self
            self.turn(turn_direction)
            self.brake()
            self.move()
            if self.collides(obj):
                collides = True
                break
            if self.velocity == 0:
                break
        self.set_state(start_state)
        return collides

    def will_go_off_track(
        self,
        max_distance_to_track: float,
        max_steps_into_future: int,
        turning_policy,
    ):
        """
        Check if car will go off track
        """
        if self.distance_to_track(self.car_simulation) > max_distance_to_track:
            return True
        start_state = self.get_state()
        went_off_track = False
        for _ in range(max_steps_into_future):
            turn_direction = turning_policy(self)  # better pass state instead of self
            self.turn(turn_direction)
            self.move()
            if self.distance_to_track(self.car_simulation) > max_distance_to_track:
                went_off_track = True
                break
            if self.velocity == 0:
                break
        self.set_state(start_state)
        return went_off_track