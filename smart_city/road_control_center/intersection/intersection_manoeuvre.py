from car.model import CarModel
from road_segments.intersection.intersection import Intersection
from smart_city.road_control_center.intersection.intersection_manoeuvres_manager import (
    IntersectionManoeuvresManager,
)
from smart_city.road_control_center.manoeuvres_preprocessing.preprocessed_manoeuvre import (
    PreprocessedManoeuvre,
)
from smart_city.schemas import IntersectionManoeuvreDescription


class IntersectionManoeuvre(PreprocessedManoeuvre):
    def __init__(
        self,
        model: CarModel,
        intersection: Intersection,
        manoeuvre_description: IntersectionManoeuvreDescription,
    ):
        self.intersection = intersection
        self.manoeuvre_description = manoeuvre_description
        super().__init__(
            IntersectionManoeuvresManager(intersection).load_manoeuvre_track_points(
                manoeuvre_description, model.name
            )
        )
