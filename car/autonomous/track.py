import math
from typing import TypeAlias

import numpy as np
from geometry import Directions, Point, Vector

TrackPath: TypeAlias = list[tuple[float, float]]


def cubic_bezier(
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


class Track:
    def __init__(self, track: list[tuple[float, float]], max_distance_in_straight_line): # 5
        self.track = track
        self.kd_tree = KDTree(track)
        self.max_distance_in_straight_line = max_distance_in_straight_line
        self.furthest_point_indexes_in_line = []
        # (
        #    self.calculate_furthest_point_indexes_in_line(max_distance_in_straight_line)
        # )

    def get_straight_track(self, start_point: Point, end_point: Point) -> TrackPath:
        distance = start_point.distance(end_point)
        x_values = np.linspace(start_point.x, end_point.x, distance + 1)
        y_values = np.linspace(start_point.y, end_point.y, distance + 1)
        return list(zip(x_values, y_values))

    def get_right_angle_turn(
        self,
        start_point: Point,
        end_point: Point,
        turn_direction: Directions,
        turn_sharpness: float = 0.66,
    ) -> TrackPath:
        if turn_direction not in [Directions.RIGHT, Directions.LEFT]:
            return []

        track_vector = Vector(end_point, start_point).get_negative_of_a_vector()
        middle_point = end_point.copy().add_vector(track_vector.scale(0.5))
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
        points_on_track = math.sqrt(2) * start_point.distance(end_point)
        return [
            cubic_bezier(t, p0, p1, p2, p3) for t in np.linspace(0, 1, points_on_track)
        ]

    def calculate_furthest_point_index_in_line(self, start_index, max_distance):
        track_points_number = len(self.track)
        if start_index >= track_points_number:
            return start_index

        start_point = self.track[start_index]
        max_end_index = start_index  # najwiekszy indeks t.z wiemy ze dziala

        furthers_possible = track_points_number - 1  # ostatni ktory moze dzialac
        while max_end_index != furthers_possible:
            end_index = (max_end_index + furthers_possible + 1) // 2
            end_point = self.track[end_index]
            a, b, c = calculate_line(start_point, end_point)

            all_points_in_line = True
            for i in range(start_index + 1, end_index):
                if distance_of_point_to_line(self.track[i], a, b, c) > max_distance:
                    all_points_in_line = False
                    break

            if not all_points_in_line:
                furthers_possible = end_index - 1
            else:
                max_end_index = end_index
        diff = max_end_index - start_index
        if diff > 180:
            return start_index + 180
        return max_end_index
        # make this 180 some variable

    def calculate_furthest_point_indexes_in_line(self, max_distance):
        res = []
        jump = 10 * max_distance
        res.append(self.calculate_furthest_point_index_in_line(0, max_distance))
        cur_index = 0  # indeks ostatniego uzupelnionego
        while cur_index < len(self.track) - 1:
            jump_index = min(cur_index + jump, len(self.track) - 1)
            furthes_point_index = self.calculate_furthest_point_index_in_line(
                jump_index, max_distance
            )
            if furthes_point_index == res[cur_index]:
                for i in range(cur_index + 1, jump_index + 1):
                    res.append(res[-1])
            else:
                for i in range(cur_index + 1, jump_index + 1):
                    res.append(
                        self.calculate_furthest_point_index_in_line(i, max_distance)
                    )
            cur_index = jump_index
        return res

    def find_distance_to_point(self, point: Point):
        distances, _ = self.kd_tree.query([point.x, point.y], k=2)
        return distances[0] + distances[1]

    def find_index_of_closest_point(self, point: Point):
        _, index = self.kd_tree.query([point.x, point.y])
        return index

    def find_straight_line_end_point(self, track_point_index):
        return self.track[self.furthest_point_indexes_in_line[track_point_index]]
