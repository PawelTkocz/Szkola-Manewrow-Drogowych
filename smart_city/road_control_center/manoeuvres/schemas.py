from typing import TypedDict

from schemas import CardinalDirection
from smart_city.road_control_center.manoeuvres.track_segment import TrackSegment


class SegmentOnManoeuvreTrackDescription(TypedDict):
    track_segment: TrackSegment
    expected_min_velocity: float | None


class IntersectionManoeuvreDescription(TypedDict):
    starting_side: CardinalDirection
    ending_side: CardinalDirection
