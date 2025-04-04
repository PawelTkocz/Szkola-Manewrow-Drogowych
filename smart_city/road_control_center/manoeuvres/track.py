from typing import TypeAlias

from geometry import Point
from scipy.spatial import KDTree

from smart_city.road_control_center.manoeuvres.schemas import (
    SegmentOnManoeuvreTrackDescription,
)
from smart_city.road_control_center.manoeuvres.segment_on_manoeuvre_track import (
    SegmentOnManoeuvreTrack,
)

TrackPath: TypeAlias = list[tuple[float, float]]


class ManoeuvreTrack:
    def __init__(
        self, track_segments_descriptions: list[SegmentOnManoeuvreTrackDescription]
    ) -> None:
        if not track_segments_descriptions:
            raise ValueError(
                "Track of a manoeuvre must contain at least one track segment."
            )
        self.track_path = []
        for track_segment_description in track_segments_descriptions:
            self.track_path.extend(track_segment_description["track_segment"])
        self.first_segment = self._get_segments_on_manoeuvre_track(
            track_segments_descriptions
        )
        self.kd_tree = KDTree(self.track_path)

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

    def get_distance_to_point(self, point: Point) -> float:
        distances, _ = self.kd_tree.query([point.x, point.y], k=2)
        return float(distances[0] + distances[1])

    def find_index_of_closest_point(self, point: Point) -> int:
        _, index = self.kd_tree.query([point.x, point.y])
        return int(index)

    def get_closest_segment_on_track(self, point: Point) -> SegmentOnManoeuvreTrack:
        index = self.find_index_of_closest_point(point)
        current_segment = self.first_segment
        while current_segment:
            if index < current_segment.cumulative_track_length:
                return current_segment
            current_segment = current_segment.next_segment_on_track
        return self.first_segment
