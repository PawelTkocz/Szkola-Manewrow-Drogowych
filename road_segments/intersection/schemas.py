from typing import TypedDict

from geometry import Directions, Rectangle


class IntersectionParts(TypedDict):
    intersection_area: Rectangle
    incoming_lines: dict[Directions, Rectangle]
    outcoming_lines: dict[Directions, Rectangle]


class IntersectionColors(TypedDict):
    street_color: str
    pavement_color: str
    lines_color: str
