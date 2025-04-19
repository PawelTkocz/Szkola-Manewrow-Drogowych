from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection, HorizontalDirection
from smart_city.road_control_center.preprocessed_manoeuvres.manoeuvre_preprocessing_manager.manoeuvre_tracks.intersection_manoeuvre_tracks.utils import (
    get_starting_position,
    get_track_end_point,
    get_track_start_point,
    get_turn_end_point,
    get_turn_start_point,
)
from smart_city.road_control_center.preprocessed_manoeuvres.manoeuvre_preprocessing_manager.manoeuvre_tracks.manoeuvre_track import (
    ManoeuvreTrack,
)
from smart_city.road_control_center.preprocessed_manoeuvres.manoeuvre_preprocessing_manager.manoeuvre_tracks.manoeuvre_track_segments.manoeuvre_track_segment import (
    ManoeuvreTrackSegment,
    TrackSegmentType,
)
from smart_city.road_control_center.preprocessed_manoeuvres.manoeuvre_preprocessing_manager.manoeuvre_tracks.manoeuvre_track_segments.right_angle_turn import (
    RightAngleTurn,
)
from smart_city.road_control_center.preprocessed_manoeuvres.manoeuvre_preprocessing_manager.manoeuvre_tracks.manoeuvre_track_segments.straight_path import (
    StraightPath,
)
from smart_city.road_control_center.preprocessed_manoeuvres.schemas import TurnSignal
from utils import clockwise_direction_shift


EXPECTED_MIN_TURN_VELOCITY = 2
END_TURN_SIGNAL_DISTANCE = 30
START_TURN_SIGNAL_DISTANCE = 150


class IntersectionTurnRightManoeuvreTrack(ManoeuvreTrack):
    def __init__(
        self, intersection: Intersection, starting_side: CardinalDirection
    ) -> None:
        super().__init__(
            self._get_track_segments(intersection, starting_side),
            get_starting_position(intersection, starting_side),
        )

    def _get_track_segments(
        self, intersection: Intersection, starting_side: CardinalDirection
    ) -> list[ManoeuvreTrackSegment]:
        ending_side = clockwise_direction_shift(starting_side, 3)
        start_point = get_track_start_point(intersection, starting_side)
        start_turn_point = get_turn_start_point(
            intersection, starting_side, ending_side
        )
        end_turn_point = get_turn_end_point(intersection, starting_side, ending_side)
        end_point = get_track_end_point(intersection, ending_side)
        return [
            StraightPath(start_point, start_turn_point),
            RightAngleTurn(
                start_turn_point,
                end_turn_point,
                HorizontalDirection.RIGHT,
                EXPECTED_MIN_TURN_VELOCITY,
            ),
            StraightPath(end_turn_point, end_point),
        ]

    def get_turn_signal(self, track_point_index: int) -> TurnSignal:
        incoming_segments_data = self.get_incoming_segments_data(track_point_index)
        if (
            incoming_segments_data["current_track_segment"].type
            == TrackSegmentType.TURN_RIGHT
        ):
            return TurnSignal.RIGHT_SIGNAL

        if (
            incoming_segments_data["next_track_segment"] is None
            and incoming_segments_data["current_track_segment_distance_covered"]
            < END_TURN_SIGNAL_DISTANCE
        ):
            return TurnSignal.RIGHT_SIGNAL

        if (
            incoming_segments_data["next_track_segment"]
            and incoming_segments_data["current_track_segment_distance_left"]
            < START_TURN_SIGNAL_DISTANCE
        ):
            return TurnSignal.RIGHT_SIGNAL
        return TurnSignal.NO_SIGNAL
