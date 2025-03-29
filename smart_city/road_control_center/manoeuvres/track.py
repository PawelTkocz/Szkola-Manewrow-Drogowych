import math
from typing import TypeAlias

import numpy as np
from geometry import Directions, Point, Vector
from scipy.spatial import KDTree

TrackPath: TypeAlias = list[tuple[float, float]]


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


def get_straight_track(start_point: Point, end_point: Point) -> TrackPath:
    distance = int(start_point.distance(end_point))
    x_values = np.linspace(start_point.x, end_point.x, distance + 1)
    y_values = np.linspace(start_point.y, end_point.y, distance + 1)
    return list(zip(x_values, y_values))


def get_right_angle_turn(
    start_point: Point,
    end_point: Point,
    turn_direction: Directions,
    turn_sharpness: float = 0.66,
) -> TrackPath:
    if turn_direction not in [Directions.RIGHT, Directions.LEFT]:
        return []

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


class Track:
    def __init__(self, track_path: TrackPath):
        self.track_path = track_path
        self.kd_tree = KDTree(track_path)

    def get_distance_to_point(self, point: Point) -> float:
        distances, _ = self.kd_tree.query([point.x, point.y], k=2)
        return float(distances[0] + distances[1])

    def find_index_of_closest_point(self, point: Point) -> int:
        _, index = self.kd_tree.query([point.x, point.y])
        return int(index)
