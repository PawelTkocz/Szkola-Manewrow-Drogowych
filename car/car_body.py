from pygame import Surface
from car.car_part import CarPart
from car.model import BodySpecification
from car.schemas import CarBodyColoristics
from geometry.direction import Direction
from geometry.vector import Point


class CarBody:
    def __init__(
        self,
        lights: list[CarPart],
        specification: BodySpecification,
        coloristics: CarBodyColoristics,
        car_front_middle: Point,
        car_direction: Direction,
    ) -> None:
        self.lights = lights
        self.shell = CarPart(
            specification["shell"],
            coloristics["shell"],
            car_front_middle,
            car_direction,
        )
        self.side_mirrors = [
            CarPart(
                position, coloristics["side_mirrors"], car_front_middle, car_direction
            )
            for position in (
                specification["left_side_mirror"],
                specification["right_side_mirror"],
            )
        ]
        self.windows = [
            CarPart(position, coloristics["windows"], car_front_middle, car_direction)
            for position in (
                specification["front_window"],
                specification["left_window"],
                specification["right_window"],
                specification["rear_window"],
            )
        ]
        self.body_parts = [self.shell] + self.side_mirrors + self.windows + self.lights

    def update_position(
        self, car_front_middle: Point, car_direction: Direction
    ) -> None:
        for part in self.body_parts:
            part.update_position(car_front_middle, car_direction)

    def draw(
        self,
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        for part in self.body_parts:
            part.draw(
                screen, scale_factor=scale_factor, screen_y_offset=screen_y_offset
            )
