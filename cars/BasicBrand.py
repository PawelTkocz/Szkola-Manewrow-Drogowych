import math

from pygame import Surface

from Geometry import Rectangle
from cars.BasicBrandDrafter import BasicBrandDrafter
from cars.Brand import Brand

# OK


class BasicBrand(Brand):
    """
    Class representing basic car brand
    """

    _width: float = 100.0
    _length_to_width_ratio = 1.8
    _length: float = _width * _length_to_width_ratio
    _max_wheels_turn: float = math.pi / 4
    _wheels_turn_speed = 0.05
    _max_velocity: float = _width / 10
    _max_acceleration: float = _width * 0.001
    _max_brake: float = _width * 0.002
    _resistance: float = _width * 0.0003

    def __init__(self, color: str = "red"):
        """
        Initialize parameters of basic brand car
        """
        self.color = color
        self.car_drafter = BasicBrandDrafter(color)

    def draw(self, body: Rectangle, wheels_angle: float, screen: Surface):
        self.car_drafter.draw(body, wheels_angle, screen)

    @property
    def width(self):
        return self._width

    @property
    def length(self):
        return self._length

    @property
    def max_wheels_turn(self):
        return self._max_wheels_turn

    @property
    def wheels_turn_speed(self):
        return self._wheels_turn_speed

    @property
    def max_velocity(self):
        return self._max_velocity

    @property
    def max_acceleration(self):
        return self._max_acceleration

    @property
    def max_brake(self):
        return self._max_brake

    @property
    def resistance(self):
        return self._resistance
