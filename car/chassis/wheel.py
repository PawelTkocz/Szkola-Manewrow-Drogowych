from car.car_part import CarPart
from car.schemas import CarPartPosition, CarPointPosition
from geometry.direction import Direction
from geometry.vector import Point


class Wheel(CarPart):
    def __init__(
        self,
        position: CarPartPosition,
        center_position: CarPointPosition,
        color: str,
        car_front_middle: Point,
        car_direction: Direction,
    ) -> None:
        super().__init__(position, color, car_front_middle, car_direction)
        self.center_position = center_position

    def update_position(
        self, car_front_middle: Point, car_direction: Direction, wheels_angle: float = 0
    ) -> None:
        super().update_position(car_front_middle, car_direction)
        wheel_middle = self._get_car_point_position(
            car_front_middle, car_direction, self.center_position
        )
        rotated_corners: list[Point] = [
            corner.rotate_over_point(wheel_middle, wheels_angle)
            for corner in self.corners
        ]
        self.corners = rotated_corners
