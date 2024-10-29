from abc import ABC, abstractmethod


class Brand:
    """
    Interface for car brand and its specifications
    """

    @property
    @abstractmethod
    def width(self):
        pass

    @property
    @abstractmethod
    def length(self):
        pass

    @abstractmethod
    def draw(self, corners, screen):
        pass
