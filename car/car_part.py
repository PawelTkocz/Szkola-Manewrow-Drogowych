from car.schemas import CarPartPosition, CarPointPosition
from geometry.direction import Direction
from geometry.shapes.polygon import Polygon
from geometry.vector import Point
from schemas import HorizontalDirection


def get_car_point_position(
    car_front_middle: Point,
    car_direction: Direction,
    relative_car_point_position: CarPointPosition,
) -> Point:
    width_vector = car_direction.get_orthogonal_vector(HorizontalDirection.RIGHT)
    length_position_vector = car_direction.copy().scale_to_len(
        relative_car_point_position["y"]
    )
    width_position_vector = width_vector.copy().scale_to_len(
        relative_car_point_position["x"]
    )
    return (
        car_front_middle.copy()
        .add_vector(length_position_vector)
        .add_vector(width_position_vector)
    )


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

    def _calculate_corners_positions(
        self, car_front_middle: Point, car_direction: Direction
    ) -> list[Point]:
        return [
            get_car_point_position(
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
