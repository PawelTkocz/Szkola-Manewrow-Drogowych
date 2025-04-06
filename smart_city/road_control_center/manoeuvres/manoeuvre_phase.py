from geometry import Point
from smart_city.road_control_center.intersection.intersection_manoeuvres.intersection_tracks import (
    TrackPointData,
)
from smart_city.road_control_center.manoeuvres.track import Track


# stop point should be passed when calculating track (with max velocities) for manoeuvre phase
class ManoeuvrePhase:
    """
    Class representing one phase of a manoeuvre.
    """

    def __init__(
        self,
        track_points_data: list[TrackPointData],
    ):
        self.track = Track(
            [
                (point_data["point"].x, point_data["point"].y)
                for point_data in track_points_data
            ]
        )
        self.max_velocities = [
            point_data["max_velocity"] for point_data in track_points_data
        ]
        self.turn_signals = [
            point_data["turn_signal"] for point_data in track_points_data
        ]

    def is_phase_over(self, front_middle_position: Point, velocity: float) -> bool:
        return False
