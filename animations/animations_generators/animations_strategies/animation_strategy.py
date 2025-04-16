from abc import ABC, abstractmethod

from car.car import Car


class AnimationStrategy(ABC):
    @abstractmethod
    def move_cars(self) -> list[Car]:
        pass

    @abstractmethod
    def handle_quit(self) -> None:
        pass
