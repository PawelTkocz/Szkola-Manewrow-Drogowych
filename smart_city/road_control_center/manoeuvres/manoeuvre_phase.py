from geometry import Point
from smart_city.road_control_center.manoeuvres.track import ManoeuvreTrack


class ManoeuvrePhase:
    """
    Class representing one phase of a manoeuvre.
    """

    stop_point_tolerance = 1

    def __init__(
        self,
        track: ManoeuvreTrack,
        stop_point: Point | None = None,
    ):
        self.track = track
        self.stop_point = stop_point

    def is_phase_over(self, front_middle_position: Point, velocity: float) -> bool:
        if not self.stop_point:
            return False
        return (
            self.stop_point.distance(front_middle_position) < self.stop_point_tolerance
            and velocity == 0
        )
