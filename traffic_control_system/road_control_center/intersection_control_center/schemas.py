from typing import TypedDict

from traffic_control_system.road_control_center.intersection_control_center.intersection_manoeuvre import (
    IntersectionManoeuvre,
)
from traffic_control_system.schemas import IntersectionManoeuvreDescription


class IntersectionManoeuvreStatus(TypedDict):
    can_safely_cross_intersection: bool


class IntersectionCarManoeuvreInfo(TypedDict):
    manoeuvre: IntersectionManoeuvre
    manoeuvre_status: IntersectionManoeuvreStatus


class IntersectionPriorityCarInfo(TypedDict):
    high_priority: bool
    velocity: float
    manoeuvre_description: IntersectionManoeuvreDescription
