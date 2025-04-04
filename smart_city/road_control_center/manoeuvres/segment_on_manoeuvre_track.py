from smart_city.road_control_center.manoeuvres.track_segment import TrackSegment


class SegmentOnManoeuvreTrack:
    def __init__(
        self,
        track_segment: TrackSegment,
        expected_min_velocity: float | None,
        *,
        previous_segment_on_track: "SegmentOnManoeuvreTrack" | None = None,
    ) -> None:
        self.track_segment: TrackSegment = track_segment
        self.next_segment_on_track: "SegmentOnManoeuvreTrack" | None = None
        self.previous_segment_on_track: "SegmentOnManoeuvreTrack" | None = None
        self.cumulative_track_length = len(track_segment.track_path)
        if previous_segment_on_track:
            self.previous_segment_on_track = previous_segment_on_track
            self.cumulative_track_length += (
                previous_segment_on_track.cumulative_track_length
            )
        self.expected_min_velocity = expected_min_velocity
