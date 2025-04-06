import math

import numpy as np
from geometry import Point, Vector
from schemas import HorizontalDirection
from smart_city.road_control_center.manoeuvres.schemas import TrackPath
from smart_city.road_control_center.manoeuvres.track_segment import (
    TrackSegment,
    TrackSegmentType,
)

TURN_SHARPNESS = 0.7


def _cubic_bezier(
    t: float, p0: Point, p1: Point, p2: Point, p3: Point
) -> tuple[float, float]:
    x = (
        (1 - t) ** 3 * p0.x
        + 3 * (1 - t) ** 2 * t * p1.x
        + 3 * (1 - t) * t**2 * p2.x
        + t**3 * p3.x
    )
    y = (
        (1 - t) ** 3 * p0.y
        + 3 * (1 - t) ** 2 * t * p1.y
        + 3 * (1 - t) * t**2 * p2.y
        + t**3 * p3.y
    )
    return x, y


class RightAngleTurn(TrackSegment):
    def __init__(
        self,
        start_point: Point,
        end_point: Point,
        turn_direction: HorizontalDirection,
    ) -> None:
        track_segment_type = (
            TrackSegmentType.TURN_LEFT
            if turn_direction == HorizontalDirection.LEFT
            else TrackSegmentType.TURN_RIGHT
        )
        super().__init__(
            track_segment_type,
            self.calculate_track_path(
                start_point, end_point, turn_direction, TURN_SHARPNESS
            ),
        )

    def calculate_track_path(
        self,
        start_point: Point,
        end_point: Point,
        turn_direction: HorizontalDirection,
        turn_sharpness: float,
    ) -> TrackPath:
        track_vector = Vector(end_point, start_point).get_negative_of_a_vector()
        middle_point = end_point.copy().add_vector(track_vector.copy().scale(0.5))
        turn_corner = middle_point.copy().add_vector(
            track_vector.get_orthogonal_vector(turn_direction).scale(0.5)
        )
        control_points = [
            start_point,
            start_point.copy().add_vector(
                Vector(turn_corner, start_point).scale(turn_sharpness)
            ),
            end_point.copy().add_vector(
                Vector(turn_corner, end_point).scale(turn_sharpness)
            ),
            end_point,
        ]
        p0, p1, p2, p3 = control_points
        points_on_track = int(math.sqrt(2) * start_point.distance(end_point))
        return [
            _cubic_bezier(t, p0, p1, p2, p3) for t in np.linspace(0, 1, points_on_track)
        ]
