from car.model import CarModel
from road_segments.intersection.intersection import Intersection

from smart_city.road_control_center.intersection.intersection_manoeuvre.intersection_tracks import (
    IntersectionTracks,
)
from smart_city.road_control_center.intersection.intersection_manoeuvre.schemas import (
    IntersectionManoeuvreDescription,
)
from smart_city.road_control_center.manoeuvres.manoeuvre import Manoeuvre


class IntersectionManoeuvre(Manoeuvre):
    def __init__(
        self,
        model: CarModel,
        intersection: Intersection,
        manoeuvre_description: IntersectionManoeuvreDescription,
    ):
        self.intersection = intersection
        self.manoeuvre_description = manoeuvre_description
        super().__init__(
            IntersectionTracks(intersection, model).get_track_points_data(
                manoeuvre_description
            )
        )
