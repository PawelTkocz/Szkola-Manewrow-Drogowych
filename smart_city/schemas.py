from typing import TypedDict

from car.model import CarModel
from geometry import Direction, Point
from schemas import CardinalDirection


class IntersectionManoeuvreDescription(TypedDict):
    starting_side: CardinalDirection
    ending_side: CardinalDirection


class CarSpecification(TypedDict):
    registry_number: str
    model: CarModel


class LiveCarState(TypedDict):
    velocity: float
    front_middle: Point
    direction: Direction
    wheels_direction: Direction
    high_priority: bool


class LiveCarData(TypedDict):
    specification: CarSpecification
    live_state: LiveCarState
    manoeuvre_description: IntersectionManoeuvreDescription | None
