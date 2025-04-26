import pygame
from geometry.direction import Direction
from geometry.shapes.rectangle import DynamicRectangle
from geometry.vector import Point


class TrafficControlElement(DynamicRectangle):
    def __init__(self, width: float, height: float) -> None:
        super().__init__(
            Point(0, 0),
            width,
            height,
            Direction(Point(0, 1)),
        )
        self._image_top_left = self.front_left
        self.rotation_angle = 0

    def update_position(self, front_middle: Point, direction: Direction) -> None:
        if not any(
            [
                direction.compare(Direction(Point(0, 1))),
                direction.compare(Direction(Point(0, -1))),
                direction.compare(Direction(Point(1, 0))),
                direction.compare(Direction(Point(-1, 0))),
            ]
        ):
            raise ValueError("Traffic control elements must by axis aligned.")
        super().update_position(front_middle, direction)
        if direction.compare(Direction(Point(0, 1))):
            self._image_top_left = self.front_left
            self.rotation_angle = 0
        elif direction.compare(Direction(Point(0, -1))):
            self._image_top_left = self.rear_right
            self.rotation_angle = 180
        elif direction.compare(Direction(Point(1, 0))):
            self._image_top_left = self.rear_left
            self.rotation_angle = 270
        else:
            self._image_top_left = self.front_right
            self.rotation_angle = 90

    def draw(
        self,
        screen: pygame.Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        raise NotImplementedError
