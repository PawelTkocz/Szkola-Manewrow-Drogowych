from typing import TypedDict

from car.model import CarModel
from geometry import Direction, Point
from smart_city.schemas import IntersectionManoeuvreDescription


class CarStartingPosition(TypedDict):
    front_middle: Point
    direction: Direction
    wheels_direction: Direction


class IntersectionAnimationCarDescription(TypedDict):
    registry_number: str
    model: CarModel
    color: str
    velocity: float
    start_frame_number: int
    manoeuvre_description: IntersectionManoeuvreDescription


class PlaybackAnimationCarDescription(TypedDict):
    registry_number: str
    model: CarModel
    color: str
    starting_position: CarStartingPosition
    velocity: float
    start_frame_number: int


class AnimationCarDescription(PlaybackAnimationCarDescription):
    manoeuvre_description: IntersectionManoeuvreDescription
