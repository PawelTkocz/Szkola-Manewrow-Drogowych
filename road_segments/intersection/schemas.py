from typing import TypedDict

from geometry.shapes.rectangle import AxisAlignedRectangle, Rectangle
from schemas import CardinalDirection


class IntersectionParts(TypedDict):
    intersection_area: AxisAlignedRectangle
    incoming_lanes: dict[CardinalDirection, Rectangle]
    outcoming_lanes: dict[CardinalDirection, Rectangle]


class IntersectionColoristics(TypedDict):
    street: str
    pavement: str
    lines: str
