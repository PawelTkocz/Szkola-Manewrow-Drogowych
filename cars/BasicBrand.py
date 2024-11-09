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

    _width: float = 50.0  # 200.0
    _length: float = 90.0  # 360
    _max_wheels_turn: float = math.pi / 4
    _wheels_turn_speed = 0.05
    _max_velocity: float = 10.0
    _max_acceleration: float = 0.1
    _max_brake: float = 1.0

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
