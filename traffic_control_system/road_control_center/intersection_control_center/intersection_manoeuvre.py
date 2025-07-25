from car.model import CarModelSpecification
from road_segments.intersection.intersection import Intersection
from traffic_control_system.road_control_center.intersection_control_center.intersection_manoeuvres_manager import (
    IntersectionManoeuvresManager,
)
from traffic_control_system.road_control_center.manoeuvres_preprocessing.preprocessed_manoeuvre import (
    PreprocessedManoeuvre,
)
from traffic_control_system.schemas import IntersectionManoeuvreDescription


class IntersectionManoeuvre(PreprocessedManoeuvre):
    def __init__(
        self,
        car_model_specification: CarModelSpecification,
        intersection: Intersection,
        manoeuvre_description: IntersectionManoeuvreDescription,
    ):
        self.intersection = intersection
        self.manoeuvre_description = manoeuvre_description
        super().__init__(
            IntersectionManoeuvresManager(intersection).load_manoeuvre_track_points(
                manoeuvre_description, car_model_specification["name"]
            )
        )
