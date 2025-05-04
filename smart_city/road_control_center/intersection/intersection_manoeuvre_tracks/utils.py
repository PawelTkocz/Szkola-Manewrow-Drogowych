from geometry.vector import Point
from road_segments.constants import LANE_WIDTH
from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection, HorizontalDirection
from smart_city.road_control_center.manoeuvres_preprocessing.schemas import (
    ManoeuvreStartCarState,
)
from utils import clockwise_direction_shift


TRACK_MARGIN_LENGTH = 100


def _get_turn_direction(
    starting_side: CardinalDirection, ending_side: CardinalDirection
) -> HorizontalDirection | None:
    if ending_side == clockwise_direction_shift(starting_side, 1):
        return HorizontalDirection.LEFT
    if ending_side == clockwise_direction_shift(starting_side, 3):
        return HorizontalDirection.RIGHT
    return None


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
    return intersection.components["incoming_lanes"][starting_side].rear_middle


def _get_turn_offset(
    intersection: Intersection, turn_direction: HorizontalDirection
) -> int:
    return int(0.5 * LANE_WIDTH) if turn_direction == HorizontalDirection.RIGHT else 0


def get_turn_start_point(
    intersection: Intersection,
    starting_side: CardinalDirection,
    ending_side: CardinalDirection,
) -> Point:
    incoming_lane = intersection.components["incoming_lanes"][starting_side]
    turn_direction = _get_turn_direction(starting_side, ending_side)
    if turn_direction is None:
        raise ValueError("Cannot compute turn start point: the track is straight.")
    start_turn_offset = _get_turn_offset(intersection, turn_direction)
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
    if turn_direction is None:
        raise ValueError("Cannot compute turn end point: the track is straight.")
    end_turn_offset = _get_turn_offset(intersection, turn_direction)
    return outcoming_lane.rear_middle.add_vector(
        outcoming_lane.direction.scale_to_len(end_turn_offset)
    )


def get_starting_position(
    intersection: Intersection, starting_side: CardinalDirection
) -> ManoeuvreStartCarState:
    incoming_lane = intersection.components["incoming_lanes"][starting_side]
    return {
        "direction": incoming_lane.direction,
        "front_middle": incoming_lane.rear_middle,
        "wheels_angle": 0,
    }
