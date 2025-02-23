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
