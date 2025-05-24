from typing import TypedDict

from schemas import CardinalDirection
from traffic_control_system.road_control_center.intersection_control_center.intersection_manoeuvre import (
    IntersectionManoeuvre,
)
from traffic_control_system.schemas import IntersectionManoeuvreDescription
from traffic_control_elements.traffic_lights.schemas import TrafficLightsState


class IntersectionManoeuvreStatus(TypedDict):
    can_safely_cross_intersection: bool


class IntersectionCarManoeuvreInfo(TypedDict):
    manoeuvre: IntersectionManoeuvre
    manoeuvre_status: IntersectionManoeuvreStatus


class IntersectionTrafficLightsState(TypedDict):
    current: dict[CardinalDirection, TrafficLightsState]
    entering_intersection_moment: dict[CardinalDirection, TrafficLightsState]


class IntersectionPriorityCarInfo(TypedDict):
    high_priority: bool
    velocity: float
    manoeuvre_description: IntersectionManoeuvreDescription
    traffic_lights_state: IntersectionTrafficLightsState
