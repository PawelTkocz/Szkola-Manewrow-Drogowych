from geometry.vector import Point
from road_segments.constants import LANE_WIDTH
from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection, HorizontalDirection
from traffic_control_system.road_control_center.manoeuvres_preprocessing.schemas import (
    ManoeuvreStartCarState,
)
from utils import clockwise_direction_shift


TRACK_MARGIN_LENGTH = 100


def _get_turn_direction(
    starting_side: CardinalDirection, ending_side: CardinalDirection
) -> HorizontalDirection:
    if ending_side == clockwise_direction_shift(starting_side, 1):
        return HorizontalDirection.LEFT
    if ending_side == clockwise_direction_shift(starting_side, 3):
        return HorizontalDirection.RIGHT
    raise ValueError("Cannot compute turn direction: the track is straight.")


def get_track_end_point(
    intersection: Intersection, ending_side: CardinalDirection
) -> Point:
    outcoming_lane = intersection.components["outcoming_lanes"][ending_side]
    return outcoming_lane.front_middle.add_vector(
        outcoming_lane.direction.scale_to_len(TRACK_MARGIN_LENGTH)
    )


def get_track_start_point(
    intersection: Intersection, starting_side: CardinalDirection
) -> Point:
    incoming_lane = intersection.components["incoming_lanes"][starting_side]
    return incoming_lane.rear_middle.add_vector(
        incoming_lane.direction.get_negative_of_a_vector().scale_to_len(
            TRACK_MARGIN_LENGTH
        )
    )


def _get_turn_offset(turn_direction: HorizontalDirection) -> int:
    return int(0.5 * LANE_WIDTH) if turn_direction == HorizontalDirection.RIGHT else 0


def get_turn_start_point(
    intersection: Intersection,
    starting_side: CardinalDirection,
    ending_side: CardinalDirection,
) -> Point:
    incoming_lane = intersection.components["incoming_lanes"][starting_side]
    turn_direction = _get_turn_direction(starting_side, ending_side)
    start_turn_offset = _get_turn_offset(turn_direction)
    return incoming_lane.front_middle.add_vector(
        incoming_lane.direction.get_negative_of_a_vector().scale_to_len(
            start_turn_offset
        )
    )


def get_turn_end_point(
    intersection: Intersection,
    starting_side: CardinalDirection,
    ending_side: CardinalDirection,
) -> Point:
    outcoming_lane = intersection.components["outcoming_lanes"][ending_side]
    turn_direction = _get_turn_direction(starting_side, ending_side)
    end_turn_offset = _get_turn_offset(turn_direction)
    return outcoming_lane.rear_middle.add_vector(
        outcoming_lane.direction.scale_to_len(end_turn_offset)
    )


def get_car_starting_position(
    intersection: Intersection, starting_side: CardinalDirection
) -> ManoeuvreStartCarState:
    incoming_lane = intersection.components["incoming_lanes"][starting_side]
    return {
        "direction": incoming_lane.direction,
        "front_middle": incoming_lane.rear_middle,
        "wheels_angle": 0,
    }
