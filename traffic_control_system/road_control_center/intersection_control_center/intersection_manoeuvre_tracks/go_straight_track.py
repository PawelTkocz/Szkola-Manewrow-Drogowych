from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from traffic_control_system.road_control_center.intersection_control_center.intersection_manoeuvre_tracks.utils import (
    get_car_starting_position,
    get_track_end_point,
    get_track_start_point,
)
from traffic_control_system.road_control_center.manoeuvres_preprocessing.manoeuvre_tracks.manoeuvre_track import (
    ManoeuvreTrack,
)
from traffic_control_system.road_control_center.manoeuvres_preprocessing.manoeuvre_tracks.manoeuvre_track_segment import (
    ManoeuvreTrackSegment,
)
from traffic_control_system.road_control_center.manoeuvres_preprocessing.manoeuvre_tracks.straight_path import (
    StraightPath,
)
from utils import clockwise_direction_shift


class IntersectionGoStraightManoeuvreTrack(ManoeuvreTrack):
    def __init__(
        self, intersection: Intersection, starting_side: CardinalDirection
    ) -> None:
        super().__init__(
            self._get_track_segments(intersection, starting_side),
            get_car_starting_position(intersection, starting_side),
        )

    def _get_track_segments(
        self, intersection: Intersection, starting_side: CardinalDirection
    ) -> list[ManoeuvreTrackSegment]:
        ending_side = clockwise_direction_shift(starting_side, 2)
        start_point = get_track_start_point(intersection, starting_side)
        end_point = get_track_end_point(intersection, ending_side)
        return [StraightPath(start_point, end_point)]
