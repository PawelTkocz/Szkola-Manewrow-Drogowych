from typing import TypedDict

from smart_city.road_control_center.preprocessed_manoeuvres.intersection_manoeuvre import (
    IntersectionManoeuvre,
)
from smart_city.schemas import IntersectionManoeuvreDescription


class IntersectionManoeuvreStatus(TypedDict):
    can_safely_cross_intersection: bool


class IntersectionCarManoeuvreInfo(TypedDict):
    manoeuvre: IntersectionManoeuvre
    manoeuvre_status: IntersectionManoeuvreStatus


class IntersectionPriorityCarInfo(TypedDict):
    high_priority: bool
    manoeuvre_description: IntersectionManoeuvreDescription
