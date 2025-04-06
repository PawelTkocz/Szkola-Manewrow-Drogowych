import numpy as np
from geometry import Point
from smart_city.road_control_center.manoeuvres.schemas import TrackPath
from smart_city.road_control_center.manoeuvres.track_segment import (
    TrackSegment,
    TrackSegmentType,
)


class StraightPath(TrackSegment):
    def __init__(
        self,
        start_point: Point,
        end_point: Point,
    ) -> None:
        super().__init__(
            TrackSegmentType.STRAIGHT_PATH,
            self.calculate_track_path(start_point, end_point),
        )

    def calculate_track_path(self, start_point: Point, end_point: Point) -> TrackPath:
        distance = int(start_point.distance(end_point))
        x_values = np.linspace(start_point.x, end_point.x, distance + 1)
        y_values = np.linspace(start_point.y, end_point.y, distance + 1)
        return list(zip(x_values, y_values))
