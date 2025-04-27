from typing import TypedDict

from car.turn_signals import TurnSignalType
from smart_city.road_control_center.manoeuvres_preprocessing.manoeuvre_tracks.manoeuvre_track_segment import (
    ManoeuvreTrackSegment,
)
from smart_city.road_control_center.manoeuvres_preprocessing.schemas import (
    ManoeuvreStartCarState,
)
from smart_city.road_control_center.track import Track


class ManoeuvreTrackSegmentData(TypedDict):
    track_segment: ManoeuvreTrackSegment
    cumulative_track_length: float


class IncomingSegmentsData(TypedDict):
    current_track_segment: ManoeuvreTrackSegment
    current_track_segment_distance_left: float
    current_track_segment_distance_covered: float
    next_track_segment: ManoeuvreTrackSegment | None


class ManoeuvreTrack(Track):
    def __init__(
        self,
        track_segments: list[ManoeuvreTrackSegment],
        start_car_state: ManoeuvreStartCarState,
    ) -> None:
        if not track_segments:
            raise ValueError(
                "Track of a manoeuvre must contain at least one track segment."
            )
        track_path = []
        for track_segment in track_segments:
            track_path.extend(track_segment.track_path)
        super().__init__(track_path)
        self.segments_data = self._get_segments_data(track_segments)
        self.start_car_state = start_car_state
        self.end_point = self.segments_data[-1]["track_segment"].end_point

    def _get_segments_data(
        self, track_segments: list[ManoeuvreTrackSegment]
    ) -> list[ManoeuvreTrackSegmentData]:
        track_segments_data: list[ManoeuvreTrackSegmentData] = []
        if not track_segments:
            return []
        track_segments_data.append(
            {
                "track_segment": track_segments[0],
                "cumulative_track_length": len(track_segments[0].track_path),
            }
        )
        for track_segment in track_segments[1:]:
            prev_track_segment = track_segments_data[-1]
            track_segments_data.append(
                {
                    "track_segment": track_segment,
                    "cumulative_track_length": len(track_segment.track_path)
                    + prev_track_segment["cumulative_track_length"],
                }
            )
        return track_segments_data

    def get_incoming_segments_data(
        self, track_point_index: int
    ) -> IncomingSegmentsData:
        current_track_index = 0
        for track_index, track_segment_data in enumerate(self.segments_data):
            if track_segment_data["cumulative_track_length"] > track_point_index:
                current_track_index = track_index
                break
        return {
            "current_track_segment": self.segments_data[current_track_index][
                "track_segment"
            ],
            "next_track_segment": self.segments_data[current_track_index + 1][
                "track_segment"
            ]
            if current_track_index + 1 < len(self.segments_data)
            else None,
            "current_track_segment_distance_left": self.segments_data[
                current_track_index
            ]["cumulative_track_length"]
            - track_point_index,
            "current_track_segment_distance_covered": track_point_index
            - (
                self.segments_data[current_track_index - 1]["cumulative_track_length"]
                if current_track_index >= 1
                else 0
            ),
        }

    def get_turn_signal(self, track_point_index: int) -> TurnSignalType:
        return TurnSignalType.NO_SIGNAL
