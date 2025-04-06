from geometry import Point
from smart_city.road_control_center.manoeuvres.schemas import TrackPath
from scipy.spatial import KDTree


class Track:
    def __init__(self, track_path: TrackPath) -> None:
        self.track_path = track_path
        self.kd_tree = KDTree(self.track_path)

    def get_distance_to_point(self, point: Point) -> float:
        distances, _ = self.kd_tree.query([point.x, point.y], k=2)
        return float(distances[0] + distances[1])

    def find_index_of_closest_point(self, point: Point) -> int:
        _, index = self.kd_tree.query([point.x, point.y])
        return int(index)
