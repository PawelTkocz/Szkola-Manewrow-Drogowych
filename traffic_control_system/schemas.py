from typing import TypedDict

from car.model import CarModelSpecification
from car.turn_signals import TurnSignalType
from geometry.direction import Direction
from geometry.vector import Point
from schemas import CardinalDirection


class IntersectionManoeuvreDescription(TypedDict):
    starting_side: CardinalDirection
    ending_side: CardinalDirection


class CarSpecification(TypedDict):
    registry_number: str
    model: CarModelSpecification


class LiveCarState(TypedDict):
    velocity: float
    front_middle: Point
    direction: Direction
    wheels_angle: float
    turn_signal: TurnSignalType
    high_priority: bool


class LiveCarData(TypedDict):
    specification: CarSpecification
    live_state: LiveCarState
    manoeuvre_description: IntersectionManoeuvreDescription | None
