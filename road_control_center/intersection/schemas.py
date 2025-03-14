from typing import TypedDict

from car.autonomous_car import CarDataTransmitter
from geometry import Directions
from manoeuvres.intersection_manoeuvre import IntersectionManoeuvre

class IntersectionManoeuvreStatus(TypedDict):
    can_safely_cross_intersection: bool

class IntersectionManoeuvreDescription(TypedDict):
    starting_side: Directions
    ending_side: Directions

class CarOnIntersection(TypedDict):
    car_data_transmitter: CarDataTransmitter
    manoeuvre: IntersectionManoeuvre
    manoeuvre_description: IntersectionManoeuvreDescription
    manoeuvre_status: IntersectionManoeuvreStatus