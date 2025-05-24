from typing import TypedDict

from car.model import CarModelSpecification
from geometry.direction import Direction
from geometry.vector import Point
from traffic_control_system.schemas import IntersectionManoeuvreDescription


class CarStartingPosition(TypedDict):
    front_middle: Point
    direction: Direction
    wheels_angle: float


class IntersectionAnimationCarDescription(TypedDict):
    registry_number: str
    model: CarModelSpecification
    color: str
    velocity: float
    start_frame_number: int
    manoeuvre_description: IntersectionManoeuvreDescription


class PlaybackAnimationCarDescription(TypedDict):
    registry_number: str
    model: CarModelSpecification
    color: str
    starting_position: CarStartingPosition
    velocity: float
    start_frame_number: int


class AnimationCarDescription(PlaybackAnimationCarDescription):
    manoeuvre_description: IntersectionManoeuvreDescription
