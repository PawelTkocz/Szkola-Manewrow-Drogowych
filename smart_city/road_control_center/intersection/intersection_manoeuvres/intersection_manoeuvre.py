from car.model import CarModel
from road_segments.intersection.intersection import Intersection

from smart_city.road_control_center.intersection.intersection_manoeuvres.intersection_tracks import (
    IntersectionTracks,
)
from smart_city.road_control_center.manoeuvres.manoeuvre import Manoeuvre
from smart_city.road_control_center.manoeuvres.manoeuvre_phase import ManoeuvrePhase
from smart_city.road_control_center.manoeuvres.schemas import (
    IntersectionManoeuvreDescription,
)


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
            [
                ManoeuvrePhase(
                    IntersectionTracks(intersection, model).get_track_points_data(
                        manoeuvre_description
                    )
                )
            ]
        )
