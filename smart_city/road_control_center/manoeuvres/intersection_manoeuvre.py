from car.model import CarModel
from geometry import Directions
from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection, HorizontalDirection, VerticalDirection

from smart_city.road_control_center.manoeuvres.manoeuvre import Manoeuvre
from smart_city.road_control_center.manoeuvres.manoeuvre_phase import ManoeuvrePhase
from smart_city.road_control_center.manoeuvres.right_angle_turn import RightAngleTurn
from smart_city.road_control_center.manoeuvres.schemas import (
    IntersectionManoeuvreDescription,
)
from smart_city.road_control_center.manoeuvres.straight_path import StraightPath
from smart_city.road_control_center.manoeuvres.track import ManoeuvreTrack

EXPECTED_MIN_TURN_VELOCITY = 2


def calculate_turn_track(
    intersection: Intersection,
    manoeuvre_description: IntersectionManoeuvreDescription,
    car_length: float,
    turn_direction: Directions,
    turn_margin: float,
) -> ManoeuvreTrack:
    starting_side = manoeuvre_description["starting_side"]
    ending_side = manoeuvre_description["ending_side"]
    incoming_line = intersection.intersection_parts["incoming_lines"][starting_side]
    start_point = incoming_line.rear_middle
    outcoming_line = intersection.intersection_parts["outcoming_lines"][ending_side]
    end_point = outcoming_line.front_middle.add_vector(
        outcoming_line.direction.scale_to_len(2 * car_length)
    )
    turn_start_point = incoming_line.front_middle.add_vector(
        incoming_line.direction.get_negative_of_a_vector().scale_to_len(turn_margin)
    )
    turn_end_point = outcoming_line.rear_middle.add_vector(
        outcoming_line.direction.scale_to_len(turn_margin)
    )
    return ManoeuvreTrack(
        [
            {
                "track_segment": StraightPath(start_point, turn_start_point),
                "expected_min_velocity": None,
            },
            {
                "track_segment": RightAngleTurn(
                    turn_start_point, turn_end_point, turn_direction
                ),
                "expected_min_velocity": EXPECTED_MIN_TURN_VELOCITY,
            },
            {
                "track_segment": StraightPath(turn_end_point, end_point),
                "expected_min_velocity": None,
            },
        ]
    )


def calculate_left_turn_track(
    intersection: Intersection,
    manoeuvre_description: IntersectionManoeuvreDescription,
    car_length: float,
) -> ManoeuvreTrack:
    return calculate_turn_track(
        intersection,
        manoeuvre_description,
        car_length,
        HorizontalDirection.LEFT,
        0,
    )


def calculate_right_turn_track(
    intersection: Intersection,
    manoeuvre_description: IntersectionManoeuvreDescription,
    car_length: float,
) -> ManoeuvreTrack:
    return calculate_turn_track(
        intersection,
        manoeuvre_description,
        car_length,
        HorizontalDirection.RIGHT,
        car_length,
    )


def calculate_straight_track(
    intersection: Intersection,
    manoeuvre_description: IntersectionManoeuvreDescription,
    car_length: float,
) -> ManoeuvreTrack:
    starting_side = manoeuvre_description["starting_side"]
    ending_side = manoeuvre_description["ending_side"]
    start_point = intersection.intersection_parts["incoming_lines"][
        starting_side
    ].rear_middle
    outcoming_lane = intersection.intersection_parts["outcoming_lines"][ending_side]
    end_point = outcoming_lane.front_middle.add_vector(
        outcoming_lane.direction.scale_to_len(2 * car_length)
    )
    return ManoeuvreTrack(
        [
            {
                "track_segment": StraightPath(start_point, end_point),
                "expected_min_velocity": None,
            }
        ]
    )


def calculate_track(
    intersection: Intersection,
    manoeuvre_description: IntersectionManoeuvreDescription,
    car_length: float,
) -> ManoeuvreTrack:
    starting_side = manoeuvre_description["starting_side"]
    ending_side = manoeuvre_description["ending_side"]
    if (starting_side in VerticalDirection and ending_side in VerticalDirection) or (
        starting_side in HorizontalDirection and ending_side in HorizontalDirection
    ):
        return calculate_straight_track(intersection, manoeuvre_description, car_length)

    directions = list(CardinalDirection)
    starting_side_index = directions.index(starting_side)
    if directions[(starting_side_index + 1) % 4] == ending_side:
        return calculate_left_turn_track(
            intersection, manoeuvre_description, car_length
        )
    else:
        return calculate_right_turn_track(
            intersection, manoeuvre_description, car_length
        )


class IntersectionManoeuvre(Manoeuvre):
    def __init__(
        self,
        model: CarModel,
        intersection: Intersection,
        manoeuvre_description: IntersectionManoeuvreDescription,
    ):
        self.intersection = intersection
        self.manoeuvre_description = manoeuvre_description
        super().__init__(
            [
                ManoeuvrePhase(
                    calculate_track(
                        intersection, manoeuvre_description, model.appearance["length"]
                    )
                )
            ]
        )
