from abc import ABC, abstractmethod
import math
from typing import TypedDict
from geometry.direction import Direction
from geometry.shapes.rectangle import DynamicRectangle
from geometry.vector import Point
from road_elements_drafter import RoadElementsDrafter


class ValidRotation(TypedDict):
    direction: Direction
    angle: float


class TrafficControlElement(DynamicRectangle, ABC):
    def __init__(self, width: float, height: float) -> None:
        super().__init__(
            Point(0, 0),
            width,
            height,
            Direction(Point(0, 1)),
        )
        self.rotation_angle = 0.0

    def update_position(self, front_middle: Point, direction: Direction) -> None:
        valid_rotations: list[ValidRotation] = [
            {"direction": Direction(Point(0, 1)), "angle": 0},
            {"direction": Direction(Point(0, -1)), "angle": math.pi},
            {"direction": Direction(Point(1, 0)), "angle": 1.5 * math.pi},
            {"direction": Direction(Point(-1, 0)), "angle": math.pi / 2},
        ]
        for valid_rotation in valid_rotations:
            if valid_rotation["direction"].compare(direction):
                super().update_position(front_middle, direction)
                self.rotation_angle = valid_rotation["angle"]
                return
        raise ValueError("Traffic control elements must by axis aligned.")

    @abstractmethod
    def draw_on_road(self, road_elements_drafter: RoadElementsDrafter) -> None:
        raise NotImplementedError
