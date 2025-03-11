from enum import Enum
from typing import Literal, TypeAlias, TypedDict

from car.car import SpeedModifications
from geometry import Directions
from intersection.intersection import Intersection
from manoeuvres.intersection_manoeuvre import IntersectionManoeuvre

class AvailableManoeuvres(Enum):
    INTERSECTION = 1
    ROUNDABOUT = 2

class MovementDecision(TypedDict):
    speed_modification: SpeedModifications
    turn_direction: Directions

class IntersectionManoeuvreDescription(TypedDict):
    type: Literal[AvailableManoeuvres.INTERSECTION]
    intersection: Intersection
    starting_side: Directions
    ending_side: Directions

ManoeuvreDescription: TypeAlias = IntersectionManoeuvreDescription
Manoeuvre: TypeAlias = IntersectionManoeuvre