import numpy as np
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from geometry import Direction, Directions, Point, Vector
from drafter.intersection import IntersectionDrafter
from animations.intersection.constants import ROAD_WIDTH

vertical = [Directions.UP, Directions.DOWN]
horizontal = [Directions.LEFT, Directions.RIGHT]


def cubic_bezier(t, p0, p1, p2, p3):
    x = (
        (1 - t) ** 3 * p0[0]
        + 3 * (1 - t) ** 2 * t * p1[0]
        + 3 * (1 - t) * t**2 * p2[0]
        + t**3 * p3[0]
    )
    y = (
        (1 - t) ** 3 * p0[1]
        + 3 * (1 - t) ** 2 * t * p1[1]
        + 3 * (1 - t) * t**2 * p2[1]
        + t**3 * p3[1]
    )
    return x, y


class StreetIntersection:
    """ """

    def __init__(self):
        self.intersection = {
            "start_roads": {
                Directions.LEFT: {
                    "point": Point(
                        SCREEN_WIDTH / 2 - ROAD_WIDTH / 2,
                        SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4,
                    ),
                    "direction": Direction(Point(1, 0)),
                },
                Directions.UP: {
                    "point": Point(
                        SCREEN_WIDTH / 2 - ROAD_WIDTH / 4,
                        SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2,
                    ),
                    "direction": Direction(Point(0, 1)),
                },
                Directions.RIGHT: {
                    "point": Point(
                        SCREEN_WIDTH / 2 + ROAD_WIDTH / 2,
                        SCREEN_HEIGHT / 2 - ROAD_WIDTH / 4,
                    ),
                    "direction": Direction(Point(-1, 0)),
                },
                Directions.DOWN: {
                    "point": Point(
                        SCREEN_WIDTH / 2 + ROAD_WIDTH / 4,
                        SCREEN_HEIGHT / 2 + ROAD_WIDTH / 2,
                    ),
                    "direction": Direction(Point(0, -1)),
                },
            },
            "end_roads": {
                Directions.LEFT: {
                    "point": Point(
                        SCREEN_WIDTH / 2 - ROAD_WIDTH / 2,
                        SCREEN_HEIGHT / 2 - ROAD_WIDTH / 4,
                    ),
                    "direction": Direction(Point(-1, 0)),
                },
                Directions.UP: {
                    "point": Point(
                        SCREEN_WIDTH / 2 + ROAD_WIDTH / 4,
                        SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2,
                    ),
                    "direction": Direction(Point(0, -1)),
                },
                Directions.RIGHT: {
                    "point": Point(
                        SCREEN_WIDTH / 2 + ROAD_WIDTH / 2,
                        SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4,
                    ),
                    "direction": Direction(Point(1, 0)),
                },
                Directions.DOWN: {
                    "point": Point(
                        SCREEN_WIDTH / 2 - ROAD_WIDTH / 4,
                        SCREEN_HEIGHT / 2 + ROAD_WIDTH / 2,
                    ),
                    "direction": Direction(Point(0, 1)),
                },
            },
        }
        self.drafter = IntersectionDrafter()

    def draw(self, screen):
        self.drafter.draw(screen)

    def get_horizontal_track(self, p: Point):
        margin = 1000
        return [(x, p.y) for x in range(-1 * margin, SCREEN_WIDTH + margin)]

    def get_vertical_track(self, p: Point):
        margin = 1000
        return [(p.x, y) for y in range(-1 * margin, SCREEN_HEIGHT + margin)]

    def get_straight_track(self, start_point: Point, end_point: Point):
        x1, y1 = start_point.x, start_point.y
        x2, y2 = end_point.x, end_point.y
        number_of_points = max(abs(x2 - x1), abs(y2 - y1)) + 1
        x_values = np.linspace(x1, x2, int(number_of_points))
        y_values = np.linspace(y1, y2, int(number_of_points))
        return list(zip(x_values, y_values))

    def get_turn_track(
        self, start_side: Directions, end_side: Directions, turn_points_vectors
    ):
        start_intersection_point = self.intersection["start_roads"][start_side]["point"]
        end_intersection_point = self.intersection["end_roads"][end_side]["point"]
        start_intersection_direction = self.intersection["start_roads"][start_side][
            "direction"
        ]
        end_intersection_direction = self.intersection["end_roads"][end_side][
            "direction"
        ]

        road_screen_margin = 1000

        start_turn_point = start_intersection_point.copy().add_vector(
            turn_points_vectors[0]
        )
        start_track_length = (
            SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2 + road_screen_margin
            if start_side in vertical
            else SCREEN_WIDTH / 2 - ROAD_WIDTH / 2 + road_screen_margin
        )
        start_track_point = start_intersection_point.copy().add_vector(
            start_intersection_direction.get_negative_of_a_vector().scale_to_len(
                start_track_length
            )
        )
        start_track_line = self.get_straight_track(start_track_point, start_turn_point)

        end_turn_point = end_intersection_point.copy().add_vector(
            turn_points_vectors[3]
        )
        end_track_length = (
            SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2 + road_screen_margin
            if end_side in vertical
            else SCREEN_WIDTH / 2 - ROAD_WIDTH / 2 + road_screen_margin
        )
        end_track_point = end_intersection_point.copy().add_vector(
            end_intersection_direction.copy().scale_to_len(end_track_length)
        )
        end_track_line = self.get_straight_track(end_turn_point, end_track_point)

        second_turn_point = start_intersection_point.copy().add_vector(
            turn_points_vectors[1]
        )
        third_turn_point = end_intersection_point.copy().add_vector(
            turn_points_vectors[2]
        )
        turn_points = [
            (start_turn_point.x, start_turn_point.y),
            (second_turn_point.x, second_turn_point.y),
            (third_turn_point.x, third_turn_point.y),
            (end_turn_point.x, end_turn_point.y),
        ]
        p0, p1, p2, p3 = turn_points
        turn_track_points = [
            cubic_bezier(t, p0, p1, p2, p3) for t in np.linspace(0, 1, 200)
        ]

        start_track_line.extend(turn_track_points)
        start_track_line.extend(end_track_line)
        return turn_points, start_track_line

    def get_short_turn_track(
        self, start_side: Directions, end_side: Directions, car_length: float
    ):
        margin = car_length
        start_intersection_direction = self.intersection["start_roads"][start_side][
            "direction"
        ]
        end_intersection_direction = self.intersection["end_roads"][end_side][
            "direction"
        ]

        start_turn_vector = (
            start_intersection_direction.get_negative_of_a_vector().scale_to_len(margin)
        )
        second_point_vector = start_intersection_direction.copy().scale_to_len(
            ROAD_WIDTH / 8 + margin * 0.2
        )
        third_point_vector = (
            end_intersection_direction.get_negative_of_a_vector()
            .scale_to_len(ROAD_WIDTH / 8)
            .add_vector(start_intersection_direction.copy().scale_to_len(0.2 * margin))
        )
        end_turn_vector = (
            end_intersection_direction.copy()
            .scale_to_len(margin)
            .add_vector(start_intersection_direction.copy().scale_to_len(0.2 * margin))
        )
        return self.get_turn_track(
            start_side,
            end_side,
            [
                start_turn_vector,
                second_point_vector,
                third_point_vector,
                end_turn_vector,
            ],
        )

    def get_long_turn_track(self, start_side: Directions, end_side: Directions):
        start_intersection_direction = self.intersection["start_roads"][start_side][
            "direction"
        ]
        end_intersection_direction = self.intersection["end_roads"][end_side][
            "direction"
        ]

        start_turn_vector = Vector(Point(0, 0))
        second_point_vector = start_intersection_direction.copy().scale_to_len(
            ROAD_WIDTH / 2
        )
        third_point_vector = (
            end_intersection_direction.get_negative_of_a_vector().scale_to_len(
                ROAD_WIDTH / 2
            )
        )
        end_turn_vector = Vector(Point(0, 0))
        return self.get_turn_track(
            start_side,
            end_side,
            [
                start_turn_vector,
                second_point_vector,
                third_point_vector,
                end_turn_vector,
            ],
        )

    def get_track_points(
        self, start_side: Directions, end_side: Directions, car_length: float
    ):
        if start_side in vertical and end_side in vertical:
            return [], self.get_vertical_track(
                self.intersection["start_roads"][start_side]["point"]
            )
        if start_side in horizontal and end_side in horizontal:
            return [], self.get_horizontal_track(
                self.intersection["start_roads"][start_side]["point"]
            )

        directions = [Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT]
        start_index = directions.index(start_side)
        end_index = directions.index(end_side)
        diff = (end_index - start_index) % 4
        if diff == 1:
            return self.get_long_turn_track(start_side, end_side)
        if diff == 3:
            return self.get_short_turn_track(start_side, end_side, car_length)

        return []

    def prepare_car_ride(
        self,
        start_side: Directions,
        end_side: Directions,
        distance_to_intersection,
        car_length: float,
    ):
        start_intersection_point = self.intersection["start_roads"][start_side]["point"]
        start_intersection_direction = self.intersection["start_roads"][start_side][
            "direction"
        ]
        start_position = start_intersection_point.copy().add_vector(
            start_intersection_direction.get_negative_of_a_vector().scale_to_len(
                distance_to_intersection
            )
        )
        _, track_points = self.get_track_points(start_side, end_side, car_length)
        return (
            start_position,
            start_intersection_direction,
            track_points,
        )
