from typing import TypedDict

from geometry.rectangle import Rectangle
from schemas import CardinalDirection


class IntersectionParts(TypedDict):
    intersection_area: Rectangle
    incoming_lanes: dict[CardinalDirection, Rectangle]
    outcoming_lanes: dict[CardinalDirection, Rectangle]


class IntersectionColoristics(TypedDict):
    street: str
    pavement: str
    lines: str
