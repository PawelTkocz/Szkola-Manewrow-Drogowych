from typing import TypedDict
from geometry import Point

from smart_city.road_control_center.manoeuvres.schemas import (
    ManoeuvreStartCarState,
)
from smart_city.road_control_center.manoeuvres.segment_on_manoeuvre_track import (
    SegmentOnManoeuvreTrack,
)
from smart_city.road_control_center.manoeuvres.track import Track
from smart_city.road_control_center.manoeuvres.track_segment import TrackSegment


class SegmentOnManoeuvreTrackDescription(TypedDict):
    track_segment: TrackSegment
    expected_min_velocity: float | None


class ManoeuvreTrack(Track):
    def __init__(
        self,
        track_segments_descriptions: list[SegmentOnManoeuvreTrackDescription],
        expected_car_start_state: ManoeuvreStartCarState,
    ) -> None:
        if not track_segments_descriptions:
            raise ValueError(
                "Track of a manoeuvre must contain at least one track segment."
            )
        track_path = []
        for track_segment_description in track_segments_descriptions:
            track_path.extend(track_segment_description["track_segment"].track_path)
        super().__init__(track_path)
        self.first_segment = self._get_segments_on_manoeuvre_track(
            track_segments_descriptions
        )
        self.expected_car_start_state = expected_car_start_state

    def _get_segments_on_manoeuvre_track(
        self, track_segments_descriptions: list[SegmentOnManoeuvreTrackDescription]
    ) -> SegmentOnManoeuvreTrack:
        first_segment = SegmentOnManoeuvreTrack(
            track_segments_descriptions[0]["track_segment"],
            track_segments_descriptions[0]["expected_min_velocity"],
        )
        current_segment = first_segment
        for track_segment_description in track_segments_descriptions[1:]:
            segment_on_track = SegmentOnManoeuvreTrack(
                track_segment_description["track_segment"],
                track_segment_description["expected_min_velocity"],
                previous_segment_on_track=current_segment,
            )
            current_segment.next_segment_on_track = segment_on_track
            current_segment = segment_on_track
        return first_segment

    def get_closest_segment_on_track(self, point: Point) -> SegmentOnManoeuvreTrack:
        index = self.find_index_of_closest_point(point)
        current_segment: SegmentOnManoeuvreTrack | None = self.first_segment
        while current_segment:
            if index < current_segment.cumulative_track_length:
                return current_segment
            current_segment = current_segment.next_segment_on_track
        return self.first_segment
