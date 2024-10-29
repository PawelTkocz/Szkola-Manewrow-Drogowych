import math

from cars.BasicBrandDrafter import BasicBrandDrafter
from cars.Brand import Brand


class BasicBrand(Brand):
    """
    Class representing basic car brand
    """

    width: float = 200.0
    length: float = 360.0
    max_wheels_turn: float = math.pi / 3
    max_velocity: float = 10.0
    max_acceleration: float = 1.0
    max_brake: float = 1.0

    def __init__(self, color: str = "red"):
        """
        Initialize parameters of basic brand car
        """
        self.color = color
        self.car_drafter = BasicBrandDrafter(self.width, self.length, color)

    def draw(self, corners, screen):
        self.car_drafter.draw(corners, screen)
