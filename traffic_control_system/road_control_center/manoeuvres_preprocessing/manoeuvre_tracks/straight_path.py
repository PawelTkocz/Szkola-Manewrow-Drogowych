import numpy as np
from geometry.vector import Point
from traffic_control_system.road_control_center.manoeuvres_preprocessing.manoeuvre_tracks.manoeuvre_track_segment import (
    ManoeuvreTrackSegment,
    TrackSegmentType,
)
from traffic_control_system.road_control_center.manoeuvres_preprocessing.schemas import (
    TrackPath,
)


class StraightPath(ManoeuvreTrackSegment):
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
