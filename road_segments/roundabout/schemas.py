from typing import TypedDict

from geometry import Circle, Rectangle
from schemas import CardinalDirection


class RoundaboutColors(TypedDict):
    street_color: str
    pavement_color: str
    lines_color: str


class RoundaboutParts(TypedDict):
    roundabout_area: Circle
    central_island: Circle
    incoming_lines: dict[CardinalDirection, Rectangle]
    outcoming_lines: dict[CardinalDirection, Rectangle]
