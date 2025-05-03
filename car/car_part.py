from car.schemas import CarPartPosition, CarPointPosition
from geometry.direction import Direction
from geometry.shapes.polygon import Polygon
from geometry.vector import Point
from schemas import HorizontalDirection


class CarPart(Polygon):
    def __init__(
        self,
        position: CarPartPosition,
        color: str,
        car_front_middle: Point,
        car_direction: Direction,
    ) -> None:
        self.relative_position = position
        super().__init__(
            self._calculate_corners_positions(car_front_middle, car_direction), color
        )

    def _get_car_point_position(
        self,
        car_front_middle: Point,
        car_direction: Direction,
        corner_relative_position: CarPointPosition,
    ) -> Point:
        """
        Based on car point position, return current point position.
        """
        width_vector = car_direction.get_orthogonal_vector(HorizontalDirection.RIGHT)
        length_position_vector = car_direction.copy().scale_to_len(
            corner_relative_position["y"]
        )
        width_position_vector = width_vector.copy().scale_to_len(
            corner_relative_position["x"]
        )
        return (
            car_front_middle.copy()
            .add_vector(length_position_vector)
            .add_vector(width_position_vector)
        )

    def _calculate_corners_positions(
        self, car_front_middle: Point, car_direction: Direction
    ) -> list[Point]:
        return [
            self._get_car_point_position(
                car_front_middle, car_direction, corner_relative_position
            )
            for corner_relative_position in self.relative_position
        ]

    def update_position(
        self, car_front_middle: Point, car_direction: Direction
    ) -> None:
        self.corners = self._calculate_corners_positions(
            car_front_middle, car_direction
        )
