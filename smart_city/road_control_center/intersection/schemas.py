from typing import TypedDict

from geometry import Directions
from manoeuvres.intersection_manoeuvre import IntersectionManoeuvre
from smart_city.schemas import LiveCarData


class IntersectionManoeuvreStatus(TypedDict):
    can_safely_cross_intersection: bool


class IntersectionManoeuvreDescription(TypedDict):
    starting_side: Directions
    ending_side: Directions


class IntersectionCarManoeuvreInfo(TypedDict):
    manoeuvre: IntersectionManoeuvre
    manoeuvre_status: IntersectionManoeuvreStatus


class IntersectionPriorityCarInfo(TypedDict):
    live_car_data: LiveCarData
    manoeuvre_description: IntersectionManoeuvreDescription
