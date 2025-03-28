from typing import TypedDict

from geometry import Directions


class IntersectionManoeuvreDescription(TypedDict):
    starting_side: Directions
    ending_side: Directions
