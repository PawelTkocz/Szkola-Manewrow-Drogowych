from scipy.spatial import KDTree

from geometry.vector import Point
from traffic_control_system.road_control_center.manoeuvres_preprocessing.schemas import (
    TrackPath,
)


class Track:
    def __init__(self, track_path: TrackPath) -> None:
        self.track_path = track_path
        self.kd_tree = KDTree(self.track_path)

    def get_distance_to_point(self, point: Point) -> float:
        distances, _ = self.kd_tree.query([point.x, point.y], k=2)
        return float(distances[0] + distances[1]) / 2

    def find_index_of_closest_point(self, point: Point) -> int:
        _, index = self.kd_tree.query([point.x, point.y])
        return int(index)
