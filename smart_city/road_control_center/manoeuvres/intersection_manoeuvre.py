from road_control_center.intersection.schemas import IntersectionManoeuvreDescription
from traffic_control_center_software.track import (
    TrackPath,
    get_right_angle_turn,
    get_straight_track,
)
from car.model import CarModel
from geometry import Directions, Point
from manoeuvres.manoeuvre import Manoeuvre
from manoeuvres.manoeuvre_phase import ManoeuvrePhase
from road_segments.intersection.intersection import Intersection

vertical = [Directions.UP, Directions.DOWN]
horizontal = [Directions.LEFT, Directions.RIGHT]
directions = [Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT]


class IntersectionManoeruvrePhase(ManoeuvrePhase):
    distance_to_finish_phase = 20

    def __init__(self, track_path: TrackPath):
        super().__init__(track_path, False, {})

    def is_phase_over(self, front_middle_position: Point, velocity: float) -> bool:
        return (
            self.track.get_distance_to_point(front_middle_position)
            < self.distance_to_finish_phase
        )


class IntersectionManoeuvre(Manoeuvre):
    def __init__(
        self,
        model: CarModel,
        intersection: Intersection,
        manoeuvre_description: IntersectionManoeuvreDescription,
    ):
        # think about not passing intersection as parameter but reading it from live_car_data.current_road_segment
        self.intersection = intersection
        self.manoeuvre_description = manoeuvre_description
        self.starting_side = manoeuvre_description["starting_side"]
        self.ending_side = manoeuvre_description["ending_side"]
        self.model = model
        super().__init__([IntersectionManoeruvrePhase(self._calculate_track_path())])

    def _calculate_track_path(self) -> TrackPath:
        if (self.starting_side in vertical and self.ending_side in vertical) or (
            self.starting_side in horizontal and self.ending_side in horizontal
        ):
            return self._calculate_straight_track_path()

        starting_side_index = directions.index(self.starting_side)
        if directions[(starting_side_index + 1) % 4] == self.ending_side:
            return self._calculate_left_turn_track_path()
        else:
            return self._calculate_right_turn_track_path()

    def _calculate_turn_track(
        self, turn_direction: Directions, turn_margin: float, turn_sharpness: float
    ) -> TrackPath:
        car_length = self.model.length
        incoming_line = self.intersection.intersection_parts["incoming_lines"][
            self.starting_side
        ]
        start_point = incoming_line.rear_middle
        outcoming_line = self.intersection.intersection_parts["outcoming_lines"][
            self.ending_side
        ]
        end_point = outcoming_line.front_middle.add_vector(
            outcoming_line.direction.scale_to_len(2 * car_length)
        )
        turn_start_point = incoming_line.front_middle.add_vector(
            incoming_line.direction.get_negative_of_a_vector().scale_to_len(turn_margin)
        )
        turn_end_point = outcoming_line.rear_middle.add_vector(
            outcoming_line.direction.scale_to_len(turn_margin)
        )
        incoming_track_path = get_straight_track(start_point, turn_start_point)
        turning_track_path = get_right_angle_turn(
            turn_start_point, turn_end_point, turn_direction, turn_sharpness
        )
        outcoming_track_path = get_straight_track(turn_end_point, end_point)
        return incoming_track_path + turning_track_path + outcoming_track_path

    def _calculate_left_turn_track_path(self):
        return self._calculate_turn_track(Directions.LEFT, 0, 0.66)

    def _calculate_right_turn_track_path(self):
        return self._calculate_turn_track(Directions.RIGHT, self.model.length, 0.66)

    def _calculate_straight_track_path(self) -> TrackPath:
        car_length = self.model.length
        start_point = self.intersection.intersection_parts["incoming_lines"][
            self.starting_side
        ].rear_middle
        outcoming_line = self.intersection.intersection_parts["outcoming_lines"][
            self.ending_side
        ]
        end_point = outcoming_line.front_middle.add_vector(
            outcoming_line.direction.scale_to_len(2 * car_length)
        )
        return get_straight_track(start_point, end_point)
