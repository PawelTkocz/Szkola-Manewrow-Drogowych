from typing import TypedDict

from car.model import CarModel
from geometry import Point
from road_control_center.intersection.schemas import IntersectionManoeuvreDescription


class LiveCarData(TypedDict):
    registry_number: int
    velocity: float
    front_middle: Point
    direction: Point
    front_left: Point
    front_right: Point
    rear_left: Point
    rear_middle: Point
    rear_right: Point
    wheels_angle: Point
    length: float
    width: float
    max_acceleration: float
    max_velocity: float
    max_brake: float
    model: CarModel
    color: str
    manoeuvre_description: IntersectionManoeuvreDescription
