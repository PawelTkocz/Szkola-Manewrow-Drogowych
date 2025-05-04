from typing import TypedDict

from geometry.shapes.rectangle import Rectangle
from schemas import CardinalDirection


class IntersectionComponents(TypedDict):
    intersection_area: Rectangle
    incoming_lanes: dict[CardinalDirection, Rectangle]
    outcoming_lanes: dict[CardinalDirection, Rectangle]


class IntersectionColors(TypedDict):
    street: str
    pavement: str
    lines: str
