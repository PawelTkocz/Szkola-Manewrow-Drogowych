from typing import TypedDict

from geometry import Circle, Directions, Rectangle


class RoundaboutColors(TypedDict):
    street_color: str
    pavement_color: str
    lines_color: str


class RoundaboutParts(TypedDict):
    roundabout_area: Circle
    central_island: Circle
    incoming_lines: dict[Directions, Rectangle]
    outcoming_lines: dict[Directions, Rectangle]
