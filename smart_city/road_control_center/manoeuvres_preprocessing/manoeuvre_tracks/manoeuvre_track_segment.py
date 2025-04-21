from enum import Enum
from geometry import Point
from smart_city.road_control_center.manoeuvres_preprocessing.schemas import TrackPath


class TrackSegmentType(Enum):
    STRAIGHT_PATH = "STRAIGHT_PATH"
    TURN_LEFT = "TURN_LEFT"
    TURN_RIGHT = "TURN_RIGHT"


class ManoeuvreTrackSegment:
    def __init__(
        self,
        type: TrackSegmentType,
        track_path: TrackPath,
        expected_min_velocity: float | None,
    ) -> None:
        self.type = type
        self.track_path = track_path
        self.expected_min_velocity = expected_min_velocity

    @property
    def start_point(self) -> Point:
        return Point(self.track_path[0][0], self.track_path[0][1])

    @property
    def end_point(self) -> Point:
        return Point(self.track_path[-1][0], self.track_path[-1][1])
