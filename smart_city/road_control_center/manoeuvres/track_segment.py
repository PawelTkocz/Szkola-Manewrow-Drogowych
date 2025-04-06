from enum import Enum
from geometry import Point
from smart_city.road_control_center.manoeuvres.schemas import TrackPath


class TrackSegmentType(Enum):
    STRAIGHT_PATH = "STRAIGHT_PATH"
    TURN_LEFT = "TURN_LEFT"
    TURN_RIGHT = "TURN_RIGHT"


class TrackSegment:
    """
    Track Segment should have such track path, that allows car to leave it
    having some expected direction and wheels angle equal to 0 - in case of
    further movement the car should hold the expected direction.
    """

    def __init__(
        self,
        type: TrackSegmentType,
        track_path: TrackPath,
    ) -> None:
        self.type = type
        self.track_path = track_path

    @property
    def start_point(self) -> Point:
        return Point(self.track_path[0][0], self.track_path[0][1])

    @property
    def end_point(self) -> Point:
        return Point(self.track_path[-1][0], self.track_path[-1][1])
