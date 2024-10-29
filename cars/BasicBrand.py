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

    _width: float = 200.0
    _length: float = 360.0
    _max_wheels_turn: float = math.pi / 3
    _max_velocity: float = 10.0
    _max_acceleration: float = 1.0
    _max_brake: float = 1.0

    def __init__(self, color: str = "red"):
        """
        Initialize parameters of basic brand car
        """
        self.color = color
        self.car_drafter = BasicBrandDrafter(self.width, self.length, color)

    def draw(self, body: Rectangle, screen: Surface):
        self.car_drafter.draw(body, screen)

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
    def max_velocity(self):
        return self._max_velocity

    @property
    def max_acceleration(self):
        return self.max_acceleration

    @property
    def max_brake(self):
        return self.max_brake
