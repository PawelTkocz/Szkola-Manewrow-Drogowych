from typing import TypedDict

from geometry import Rectangle
from schemas import CardinalDirection


class IntersectionParts(TypedDict):
    intersection_area: Rectangle
    incoming_lines: dict[CardinalDirection, Rectangle]
    outcoming_lines: dict[CardinalDirection, Rectangle]


class IntersectionColors(TypedDict):
    street_color: str
    pavement_color: str
    lines_color: str
