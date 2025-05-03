from geometry.direction import Direction
from geometry.shapes.rectangle import DynamicRectangle
from geometry.vector import Point
from road_elements_drafter import RoadElementsDrafter


class TrafficControlElement(DynamicRectangle):
    def __init__(self, width: float, height: float) -> None:
        super().__init__(
            Point(0, 0),
            width,
            height,
            Direction(Point(0, 1)),
        )
        self._image_center = self.center
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
            self._image_center = self.center
            self.rotation_angle = 0
        elif direction.compare(Direction(Point(0, -1))):
            self._image_center = self.center
            self.rotation_angle = 180
        elif direction.compare(Direction(Point(1, 0))):
            self._image_center = self.center
            self.rotation_angle = 270
        else:
            self._image_center = self.center
            self.rotation_angle = 90

    def draw_on_road(self, road_elements_drafter: RoadElementsDrafter) -> None:
        raise NotImplementedError
