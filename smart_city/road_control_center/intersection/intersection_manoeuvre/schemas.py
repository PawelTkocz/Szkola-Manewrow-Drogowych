from typing import TypedDict
from schemas import CardinalDirection


class IntersectionManoeuvreDescription(TypedDict):
    starting_side: CardinalDirection
    ending_side: CardinalDirection
