from typing import TypeAlias, TypedDict

from geometry import Direction, Point
from schemas import CardinalDirection

TrackPath: TypeAlias = list[tuple[float, float]]


class ManoeuvreStartCarState(TypedDict):
    front_middle: Point
    direction: Direction
    wheels_direction: Direction


class IntersectionManoeuvreDescription(TypedDict):
    starting_side: CardinalDirection
    ending_side: CardinalDirection
