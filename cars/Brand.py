from abc import ABC, abstractmethod
from pygame import Surface
from Geometry import Rectangle

# OK


class Brand(ABC):
    """
    Interface for car brand and its specifications

    Each car brand class must specify basic car properties like
    width, length, maximum velocity etc and how the car looks
    """

    @property
    @abstractmethod
    def width(self):
        pass

    @property
    @abstractmethod
    def length(self):
        pass

    @property
    @abstractmethod
    def max_wheels_turn(self):
        pass

    @property
    @abstractmethod
    def wheels_turn_speed(self):
        pass

    @property
    @abstractmethod
    def max_velocity(self):
        pass

    @property
    @abstractmethod
    def max_acceleration(self):
        pass

    @property
    @abstractmethod
    def max_brake(self):
        pass

    @property
    @abstractmethod
    def resistance(self):
        pass

    @abstractmethod
    def draw(self, body: Rectangle, wheels_angle: float, screen: Surface):
        pass
