from typing import TypedDict

from car.autonomous.program import AutonomousDrivingProgram
from car.autonomous.schemas import Manoeuvre
from car.car import RoadSegment
from car.model import CarModel
from geometry import Point


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
    road_segment: RoadSegment
    autonomous_driving_program: AutonomousDrivingProgram | None
    current_manoeuvre: Manoeuvre | None